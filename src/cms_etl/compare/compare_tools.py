"""This module contains functions that compare dataframes and return the results."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable, Dict

import pandas as pd
from rapidfuzz import fuzz, process
from rapidfuzz.utils import default_process
from rich.columns import Columns

from cms_etl.utils import console

if TYPE_CHECKING:
    pass


def filter_by_lead_digits(df: pd.DataFrame, col: str, compare_str: str) -> pd.DataFrame | None:
    """Return a DataFrame containing the rows
    where the leading digits of the address column
    match the leading digits of the compare string.
    """
    try:
        lead_digits = re.match(r"^(\d+)", compare_str.strip())
        if not lead_digits:
            alpha_match = filter_df_by_lead_alpha(df, col, compare_str)
            # print(alpha_match)
            return alpha_match
        return df[
            df[col]
            .astype(str)
            .str.extract(
                r"^(\d+)"  # Extract leading digits ^: start of string, \d: digit, +: one or more
            )
            .fillna(-1)
            .astype(int)  # Convert to integer
            .eq(int(lead_digits.group()))
            .any(axis=1)
        ]
    except (ValueError, AttributeError) as e:
        console.log(f"ValueError in filter lead digits: {e}")
    return None


def filter_by_value(df: pd.DataFrame, col: str, value: object) -> pd.DataFrame | None:
    """Return a DataFrame containing the rows
    where the value of the address column
    matches the compare value.
    """
    if isinstance(value, str):
        return df[df[col].str.strip().eq(value)]
    if isinstance(value, (int, float, bool)):
        return df[df[col].eq(value)]
    return None


def filter_df_by_lead_alpha(df: pd.DataFrame, col: str, compare_str: str) -> pd.DataFrame | None:
    """Return a DataFrame containing the rows
    where the leading characters of the address column
    are letters and match the leading characters of the compare string.
    """
    df = df.copy(deep=True)
    comp_lead_alpha = re.match(r"^[a-zA-Z]+", compare_str.strip())
    if not comp_lead_alpha:
        return None
    return df[
        df[col]
        .astype(str)
        .str.extract(
            r"^[a-zA-Z]+"
        )  # Extract leading letters ^: start of string, [a-zA-Z]: any letter, +: one or more
        .eq(comp_lead_alpha.group())
        .any(axis=1)
    ]


def fuzz_against_col(df: pd.DataFrame, col: str, compare_str: str, fuzz_type: str) -> dict | None:
    """Return a DataFrame containing the rows
    where the address column matches the compare string
    using fuzzy matching.
    """

    compare_str = compare_str.lower().strip()

    fuzzy_func = get_algo_dict().get(fuzz_type, fuzz.ratio)
    fuzzed_col = df[col].apply(lambda x: fuzzy_func(x, compare_str, processor=default_process))

    matches = df[fuzzed_col.gt(80)]
    if matches.empty:
        return None
    if matches.shape[0] == 1:
        return df[matches].to_dict()
    if matches.shape[0] > 1:
        console.rule("Multiple matches found. Please select one.")
        console.print(matches)
        idx_choice = console.input(
            "Enter the index of the row you want to select (nothing to reject all): "
        )
        if idx_choice:
            try:
                return matches.iloc[int(idx_choice)].to_dict()
            except IndexError:
                console.log("Invalid index. Please try again.")
    return None


def fuzz_col_w_process(
    df: pd.DataFrame, source_row: pd.Series, col: str, src_str: str, fuzz_type: str
) -> dict | None:
    """Return a DataFrame containing the rows
    where the address column matches the compare string"""
    # add incr index to df
    df = df.reset_index(drop=True)

    processed_src_str = default_process(src_str.strip())
    scorer = get_algo_dict().get(fuzz_type, fuzz.ratio)

    fuzzy_match = process.extract(
        processed_src_str,
        df[col].values.tolist(),
        scorer=scorer,
        processor=default_process,
        score_cutoff=80,
    )

    if not fuzzy_match:
        return None

    if fuzzy_match[0][1] > 86 and (len(fuzzy_match) == 1 or fuzzy_match[1][1] < 86):
        try:
            match = df[df[col].eq(fuzzy_match[0][0])]
            # console.log(match)
            for _, row in match.iterrows():
                return row.to_dict()
        except (IndexError, ValueError) as e:
            console.log(f"Invalid index. Please try again. Error: {e}")
    elif fuzzy_match[0][1] > 86 and fuzzy_match[1][1] > 86:
        console.clear()
        console.rule("Multiple matches found. Please select one.")
        console.print(f"[bold]Source string: {src_str}[/bold]", justify="center")
        console.print(source_row, justify="center", style="bold on blue")
        console.print("\n")
        columns = []
        idx_choice = None
        try:
            for i, match in enumerate(fuzzy_match):
                columns.append(f"{i+1}. {match}\n{df.loc[match[2]]}")
            console.print(Columns(columns, padding=(2, 2)), justify="center")
            idx_choice = console.input(
                "Enter the index of the row you want to select (nothing to reject all): "
            )
        except IndexError as e:
            console.log(f"Invalid index. {e}")
        except ValueError as e:
            console.log(f"Invalid value. {e}")

        if idx_choice is None:
            return None

        try:
            chosen = df[df[col].eq(fuzzy_match[int(idx_choice) - 1][0])]
            # return dict of the chosen row
            for _, row in chosen.iterrows():
                return row.to_dict()
        except (IndexError, ValueError) as e:
            console.log(f"Invalid index. Please try again. Error: {e}")
        return None
    return None


def get_algo_dict() -> Dict[str, Callable]:
    """Return a dictionary of fuzzy matching algorithms."""
    return {
        "ratio": fuzz.ratio,
        "partial_ratio": fuzz.partial_ratio,
        "token_ratio": fuzz.token_ratio,
        "token_set": fuzz.token_set_ratio,
        "token_sort": fuzz.token_sort_ratio,
        "partial_token_set": fuzz.partial_token_set_ratio,
        "partial_token_sort": fuzz.partial_token_sort_ratio,
        "partial_ratio_alignment": fuzz.partial_ratio_alignment,
        "w_ratio": fuzz.WRatio,
        "q_ratio": fuzz.QRatio,
    }


def split_address_lines(df: pd.DataFrame, src_col: str, addr_line2_col: str) -> pd.DataFrame:
    """Split the address column into two columns based on keywords (Suite, Ste, Unit, #, etc)."""
    df[addr_line2_col] = df[src_col].str.extract(r"((?:SUITE|STE|UNIT|#)\s\d+.*)", flags=re.I)
    df[src_col] = df[src_col].str.replace(r"(SUITE|STE|UNIT|#)\s\d+.*", "", flags=re.I)
    return df
