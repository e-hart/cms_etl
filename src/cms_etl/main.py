"""Main module for the cms_etl application."""

import argparse
from typing import Any, Dict

from cms_etl.app_context import AppContext
from cms_etl.db.adapters.config import MySQLConfig

# TODO: Add logging
# TODO: Implement config file for database credentials
# TODO?: Decouple command stack from command execution
# TODO: PANDASGUI needs to be removed. Replace with web-based viewer?


def main():
    """
    Main entry point for the interactive environment.
    """
    parser = argparse.ArgumentParser(description="Process database credentials.")
    parser.add_argument("--user", type=str, required=False, help="Database user")
    parser.add_argument("--password", type=str, required=False, help="Database password")
    parser.add_argument("--host", type=str, required=False, help="Database host")
    parser.add_argument("--db_name", type=str, required=False, help="Database name")

    args = parser.parse_args()

    db_creds: Dict[str, Any] = {
        "user": args.user,
        "password": args.password,
        "host": args.host,
        "db_name": args.db_name,
    }

    ctx = None

    db_cfg = MySQLConfig(**db_creds) if all(db_creds.values()) else None
    ctx = AppContext(db_cfg)
    ctx.menu_ctrlr.run_main_menu()


if __name__ == "__main__":
    main()
