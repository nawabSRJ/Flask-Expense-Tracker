import pymysql
import pymysql.cursors

DB_CONFIG = {
    "host":        "localhost",
    "user":        "root",
    "password":    "",
    "database":    "Expense_App",
    "charset":     "utf8mb4",
    "autocommit":  True,
    "cursorclass": pymysql.cursors.DictCursor,
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)