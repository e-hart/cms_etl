import pandas as pd
from cms_etl.table.commands.split_address import SplitAddressLinesCommand
from cms_etl.table.table import Table


def test_split_addres_lines_command():
    """Test the SplitAddressLinesCommand class."""
    addresses = [
        "123 Main St",
        "456 Elm St Suite 101",
        "789 Oak St Apt 202",
        "101 Pine St, Room 303",
        "202 Maple St Building 4",
        "303 Birch St Bldg 5 Floor 6",
        "404 Cedar St # 707",
        "505 Walnut St Ste. 808",
        "606 Cherry St Ste 909",
        "707 Peach St Unit 1010",
    ]
    addr_line1_col = "address_line1"
    addr_line2_col = "address_line2"
    df = pd.DataFrame({"address_line1": addresses, "address_line2": ["" for _ in addresses]})
    table = Table(df.copy(deep=True), "test_table")
    cmd = SplitAddressLinesCommand(table, addr_line1_col, addr_line2_col)
    assert cmd.addr_src_col == addr_line1_col
    assert cmd.addr_line2_col == addr_line2_col
    assert cmd._cmd_args == {  # pylint: disable=protected-access
        "addr_src_col": addr_line1_col,
        "addr_line2_col": addr_line2_col,
    }
    cmd.execute()
    # print("\n", table.df)
    assert table.df[addr_line1_col].equals(
        pd.Series(
            [
                "123 Main St",
                "456 Elm St",
                "789 Oak St",
                "101 Pine St",
                "202 Maple St",
                "303 Birch St",
                "404 Cedar St",
                "505 Walnut St",
                "606 Cherry St",
                "707 Peach St",
            ]
        )
    )
    assert table.df[addr_line2_col].equals(
        pd.Series(
            [
                "",
                "Suite 101",
                "Apt 202",
                "Room 303",
                "Building 4",
                "Bldg 5 Floor 6",
                "# 707",
                "Ste. 808",
                "Ste 909",
                "Unit 1010",
            ]
        )
    )
    cmd.undo()
    assert table.df.equals(df)
