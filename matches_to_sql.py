import argparse
import json
from pathlib import Path


def generate_sql(json_data, table_name: str) -> str:
    sql_statements = []
    sql_start = f"INSERT INTO {table_name} (profile_id, cms_id, category_id) VALUES"
    sql_end = "ON DUPLICATE KEY UPDATE cms_id = VALUES(cms_id);"

    values_list = []
    for entry in json_data:
        cms_info = entry.get("cms", {})
        profile_id = cms_info.get("profile_id", "NULL")
        cms_id = cms_info.get("CMS Certification Number (CCN)", "NULL")
        category_id = cms_info.get("category_id", "NULL")
        values_list.append(f"({profile_id}, {cms_id}, {category_id})")

    sql_values = ",\n".join(values_list)
    sql_statements.append(f"{sql_start}\n{sql_values}\n{sql_end}")
    return "\n".join(sql_statements)


def main(input_file_path: str, table_name: str) -> None:
    """Generate SQL statements from a JSON file."""
    input_path = Path(input_file_path)
    output_file_path = input_path.with_suffix(".sql")

    try:
        with open(input_path, "r", newline="", encoding="utf-8") as file:
            json_data = json.load(file)

        sql_output = generate_sql(json_data, table_name)

        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(sql_output)
        print(f"SQL file generated: {output_file_path}")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate SQL statements from JSON output of cms_etl matcher."
    )
    parser.add_argument(
        "input_file_path", type=str, required=True, help="Path to the input JSON file."
    )
    parser.add_argument(
        "--table", type=str, required=True, help="Table name for the SQL statements."
    )
    args = parser.parse_args()
    main(args.input_file_path, args.table)
