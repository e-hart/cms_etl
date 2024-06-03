"""Compare Tables Menu."""

from __future__ import annotations

import json
from time import time
from typing import TYPE_CHECKING, Optional

import pandas as pd
from rapidfuzz import fuzz
from rich.columns import Columns

from cms_etl.compare import compare_tools
from cms_etl.menu import BaseMenu, MenuOption
from cms_etl.utils import console

if TYPE_CHECKING:
    from cms_etl.app_context import AppContext
    from cms_etl.table.table import Table


class CompareTablesMenu(BaseMenu):
    """Compare Table Menu."""

    def __init__(
        self,
        ctx: AppContext,
        title: str,
        *,
        table1: Optional[Table] = None,
        table2: Optional[Table] = None,
    ):
        super().__init__(ctx, title)
        self.table1: Table | None = table1
        self.table2: Table | None = table2
        self._col_name_t1: str = ""
        self._col_name_t2: str = ""

    def _set_options(self):
        """Set menu options."""
        base_options = [
            MenuOption(name="Select Tables for Comparison", action=self.select_tables),
        ]

        conditional_options = [MenuOption(name="Fuzzy Match Columns", action=self.fuzz_col_vs_col)]

        back = [MenuOption(name="Back", action=self.back)]
        self.options = []
        self.options.append(*base_options)
        if self.table1 and self.table2:
            self.options.append(*conditional_options)
        self.options.append(*back)

    def select_tables(self):
        """Select Tables for Comparison."""
        console.rule("Select Tables for Comparison")
        tables = list(self.ctx.table_mgr.list_tables())
        if not tables:
            console.print("No tables available for comparison.")
            return
        for i, table in enumerate(tables, start=1):
            console.print(f"{i}. {table.name}")
        try:
            choice = int(console.input("Enter the number of the first table: "))
            self.table1 = tables[choice - 1]
            choice = int(console.input("Enter the number of the second table: "))

            self.table2 = tables[choice - 1]
        except (IndexError, ValueError):
            console.print("Invalid choice.")
        if self.table1 and self.table2:
            console.print(
                f"Tables '{self.table1.name}' and '{self.table2.name}' selected for comparison."
            )
        cur_menu = self.ctx.menu_ctrlr.menu_stack.peek()
        cur_menu[2]["table1"] = self.table1
        cur_menu[2]["table2"] = self.table2

    def compare_tables(self):
        """Compare the selected tables."""
        self.ctx.menu_ctrlr.open_menu(
            self.menus.compare_tables,
            "Compare Tables",
            table1=self.table1,
            table2=self.table2,
        )

    def _select_column(self, table_num: int):
        """Select a column."""
        table = self.table1 if table_num == 1 else self.table2

        if not table:
            console.print("Table not selected.")
            return

        console.rule(f"Select Column from `{table.name}`")
        columns = list(table.df.columns)
        for i, column in enumerate(columns, start=1):
            console.print(f"{i}. {column}")
        print("\n")
        choice = console.input("Enter the number of the column to select: ")
        print("\n")
        try:
            column = columns[int(choice) - 1]
            if table_num == 1:
                self._col_name_t1 = column
            else:
                self._col_name_t2 = column
            console.print(f"Selected column: {column}")
        except (IndexError, ValueError):
            console.print("Invalid choice.")

    def select_columns(self):
        """Select columns for comparison."""
        self._select_column(1)
        self._select_column(2)

    def fuzz_col_vs_col(self):
        """Fuzzy match columns."""
        if not self.table1 or not self.table2:
            console.print("Tables not selected.")
            return
        self.select_columns()

        matches = []
        are_addrs = "address" in self._col_name_t1.lower() or "address" in self._col_name_t2.lower()
        for _, row in self.table1.df.iterrows():
            try:
                if are_addrs:
                    t1_col_list = list(self.table1.df.columns)
                    t1_addr_line2_col = t1_col_list.index(self._col_name_t1) + 1
                    t2_col_list = list(self.table2.df.columns)
                    t2_addr_line2_col_idx = t2_col_list.index(self._col_name_t2) + 1
                    t2_addr_line2_col = t2_col_list[t2_addr_line2_col_idx]
                    t1_zip_col = [
                        col for col in t1_col_list if "zip" in col.lower() and "code" in col.lower()
                    ][0]
                    t2_zip_col = [
                        col for col in t2_col_list if "zip" in col.lower() and "code" in col.lower()
                    ][0]

                    filtered = compare_tools.filter_by_value(
                        self.table2.df.copy(deep=True), t2_zip_col, str(row[t1_zip_col])
                    )

                    if filtered is None or filtered.empty:
                        continue

                    filtered = compare_tools.filter_by_lead_digits(
                        filtered, self._col_name_t2, row[self._col_name_t1]
                    )

                    if filtered is None or filtered.empty:
                        continue

                    match = compare_tools.fuzz_col_w_process(
                        filtered.copy(),
                        row,
                        self._col_name_t2,
                        row[self._col_name_t1],
                        "token_set",
                    )

                    if match:
                        t1_addr_line2 = (
                            str(row.iloc[t1_addr_line2_col]).strip()
                            if row.iloc[t1_addr_line2_col]
                            else ""
                        )

                        t2_addr_line2 = (
                            str(match[t2_addr_line2_col]).strip()
                            if match[t2_addr_line2_col] not in [" ", "  ", "   "]
                            and match[t2_addr_line2_col] is not None
                            else ""
                        )

                        fuzz_line2 = fuzz.token_set_ratio(
                            t1_addr_line2,
                            t2_addr_line2,
                            processor=compare_tools.default_process,
                        )

                        if fuzz_line2 > 86 or (t1_addr_line2 == t2_addr_line2):
                            matches.append([row.to_dict(), match])
                        else:
                            self.clear()
                            console.rule(
                                f"Line 2 validation failed: `'{row[self._col_name_t1]}' [bold]'{t1_addr_line2}'[/bold]` vs. `'{match.get(self._col_name_t2)}' [bold]'{t2_addr_line2}'[/bold]`"
                            )
                            console.print(
                                Columns([str(row), str(pd.Series(match))], padding=(4, 2)),
                                justify="center",
                            )
                            choice = console.input("Enter 'y' to keep the match: ")
                            if choice.lower() == "y":
                                matches.append([row.to_dict(), match])

                else:
                    match = compare_tools.fuzz_col_w_process(
                        self.table2.df,
                        row,
                        self._col_name_t2,
                        row[self._col_name_t1],
                        "token_set",
                    )
                    if match:
                        matches.append([row.to_dict(), match])
            except (ValueError, IndexError, KeyError, Exception) as e:
                console.print(f"Error in compare_tables.fuzz_col_vs_col: {e}")
                raise e

        # console.print(matches)
        for match in matches:
            console.rule()
            console.print(
                Columns(
                    [
                        str(pd.Series(match[0])),
                        "|\n|\n|\n|\n|\n|\n|\n|\n|\n",
                        str(pd.Series(match[1])),
                    ],
                    padding=(6, 6),
                ),
                style="white on blue",
                justify="center",
            )

        matches_list = []
        for match in matches:
            matches_list.append(
                {
                    self.table1.metadata["source_type"]: match[0],
                    self.table2.metadata["source_type"]: match[1],
                }
            )
            for table in [self.table1, self.table2]:
                if table.metadata.get("s1_category_id"):
                    matches_list[-1]["cms"]["category_id"] = table.metadata["s1_category_id"]

        console.print(matches_list)
        cat_id = self.table1.metadata.get("s1_category_id") or self.table2.metadata.get(
            "s1_category_id"
        )
        # write matches to file:
        with open(f"matches_{cat_id}_{int(time())}.json", "w", encoding="utf-8") as f:
            for i, mat in enumerate(matches_list):
                mat["cms"]["profile_id"] = mat["db"]["id"]
                matches_list[i] = mat
            f.write(json.dumps(matches_list, indent=2))

        console.print("Matches written to matches.json")
