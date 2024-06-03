"""Module to render tables"""

import os
from typing import Literal

from cms_etl.table.table import Table
from cms_etl.utils import console


def render_table(table: Table, to: Literal["console", "html", "md"] = "console"):
    """Render a table."""
    match to:
        case "console":
            console.print(table)
        case "html":
            html = table.df.to_html()
            if not os.path.exists("tmp"):
                os.makedirs("tmp")
            file_path = f"tmp/{table.name}.html"
            file_path = os.path.abspath(file_path)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html)
            console.print(f"Table saved to: {file_path}")
            return file_path
        case "md":
            md = table.df.to_markdown()
            if not os.path.exists("tmp"):
                os.makedirs("tmp")
            with open(f"tmp/{table.name}.md", "w", encoding="utf-8") as file:
                file.write(md)
