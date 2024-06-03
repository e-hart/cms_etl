"""Module to define the SplitAddressCommand class."""

import json
from dataclasses import dataclass

from cms_etl.table.base_command import Command
from cms_etl.utils import console, get_cmd_args


@dataclass
class SplitAddressLinesCommand(Command):
    """Command to split an address column into line 1 and line 2."""

    addr_src_col: str
    addr_line2_col: str

    def __post_init__(self):
        self._cmd_args = get_cmd_args(self)
        self._og_df = self.table.df.copy(deep=True)

    def execute(self):
        """Execute the command."""
        regex_pattern = self.__get_addr_split_re_ptrn()
        # Split the address column into two columns
        self.table.df[[self.addr_src_col, self.addr_line2_col]] = self.table.df[
            self.addr_src_col
        ].str.split(regex_pattern, n=1, expand=True, regex=True)
        # Strip the whitespace from the columns
        self.table.df[self.addr_src_col] = self.table.df[self.addr_src_col].str.strip()
        self.table.df[self.addr_line2_col] = (
            self.table.df[self.addr_line2_col].str.strip().fillna("")
        )

    def undo(self):
        """Undo the command."""
        self.table.df = self._og_df.copy(deep=True)
        console.print(f"Undone: {json.dumps(self.serialize(), indent=4)}")

    def __get_addr_split_re_ptrn(self) -> str:
        """Return the regex pattern to split the address."""
        split_terms = [
            r"suite",
            r"ste.",
            r"ste",
            r"unit",
            r"apt",
            r"room",
            r"building",
            r"bldg",
            r"floor",
            r"p.o.box",
            r"p.o. box",
            r"po box",
        ]
        regex_str = r"(?i),|(?= #)|\b(?=" + "|".join(split_terms) + r")\b"
        return regex_str
