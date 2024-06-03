"""Table Loader menu."""

import os
from concurrent import futures

import requests

from cms_etl.menu import BaseMenu, MenuOption
from cms_etl.models.cms_meta_res import CMSMetaResponse
from cms_etl.utils import Pick, console, select_from_list


class LoadDataMenu(BaseMenu):
    """Table Loader menu."""

    # MARK: - Menu Setup
    def _set_options(self):
        self.options = [
            MenuOption(name="Load Table from CSV", action=self.load_from_csv),
            MenuOption(name="Load Table from Database", action=self.load_from_db),
            MenuOption(
                name="Load Table from CMS Source",
                action=self.load_from_cms_source,
            ),
            MenuOption(name="Back", action=self.back),
        ]

    # MARK: - CSV Loader
    def load_from_csv(self):
        """Add a Table from a CSV file."""
        file_path = console.input(f"Enter CSV file path relative to {os.getcwd()}: ")
        abs_path = os.path.abspath(file_path)
        try:
            # Load the Table from the CSV file
            df = self.ctx.data_loader.load_csv(abs_path)
            name = console.input("Enter a name for the Table: ")
            description = console.input("Enter a description for the Table: ")
            # Add the Table to the DataFrameManager

            rename_columns = console.input("Would you like to rename the columns? (y/n): ")
            if rename_columns.lower() == "y":
                columns = list(df.columns)
                for _, column in enumerate(columns, start=1):
                    new_name = console.input(f"Enter a new name for column '{column}': ")
                    df.rename(columns={column: new_name}, inplace=True)
            # self.__choose_idx_col(df)
            self.ctx.table_mgr.add_table(
                df, name, description, source_type="csv", file_path=abs_path
            )
            console.print("Table added successfully!")
        except FileNotFoundError:
            console.print("File not found!")

    # MARK: - Database Loader
    def load_from_db(self):
        """Add a Table from a database table."""

        db_key = select_from_list(
            Pick.one,
            self.ctx.db_mgr.list_dbs(),
            title="Databases",
            prompt="Choose a database (by index): ",
        )

        if db_key is None or not isinstance(db_key, str):
            return

        t_name = select_from_list(
            Pick.one,
            self.ctx.db_mgr[db_key].list_tables(),
            title=f"Tables in `{db_key}`",
            prompt="Choose a table (by index): ",
            max_col_len=20,
        )

        if not isinstance(t_name, str):
            return

        console.print(f"Loading table '{t_name}' from database '{db_key}'...")

        df = self.ctx.data_loader.load_from_db(t_name, db_key)

        if df is None:
            console.print("Failed to load table.")
            return

        name = console.input(f"Enter a name for the Table ({t_name}):") or t_name
        description = console.input("Enter a description for the Table: ")

        self.ctx.table_mgr.add_table(
            df, name, description, db_key=db_key, db_table_name=t_name, source_type="db"
        )

        console.print("Table added successfully!")

    # MARK: - CMS Loader
    def load_from_cms_source(self):
        """Add a Table from a CMS source."""

        category = select_from_list(
            Pick.one,
            list(self.ctx.data_loader.cms_loader.get_categories()),
            title="CMS Categories",
            prompt="\nChoose category: ",
        )

        if category is None or not isinstance(category, str):
            return

        source_meta_urls = self.ctx.data_loader.cms_loader.get_cat_sources(category)

        def get_source_meta(url: str):
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return CMSMetaResponse(**response.json())

        with futures.ThreadPoolExecutor() as executor:
            source_metas = list(executor.map(get_source_meta, source_meta_urls))

        source_names: list[str] = [source.title for source in source_metas]

        source_choice = select_from_list(
            Pick.one,
            source_names,
            title=f"Sources in Category '{category}'",
            prompt="Choose dataset: ",
        )

        if source_choice is None or not isinstance(source_choice, str):
            return

        source = list(source_metas)[source_names.index(source_choice)]

        print("\n")
        try:
            dataset1 = self.ctx.data_loader.cms_loader.get_dataset(category, source)
            if dataset1 is None:
                console.print("Failed to load dataset.")
                return
            df, metadata = dataset1
            console.print(df)

            name = console.input(f"Enter a name for the Table ({source.title}): ") or source.title

            description = console.input("Enter a description for the Table: ")

            self.ctx.table_mgr.add_table(
                df,
                name,
                description,
                **metadata,
            )

            self.clear()
            console.print("Table added successfully!")

        except (ValueError, KeyError) as e:
            console.print(f"Failed to load table: {e}")
        except Exception as e:
            console.print(f"An error occurred: {e}")
            raise e
