from cms_etl.db.adapters.config import MySQLConfig

db_test_config = MySQLConfig(
    db_name="senior-one-prod",
    user="root",
    password="example",
    host="localhost",
    port=3306,
)
