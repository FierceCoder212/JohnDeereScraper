import sqlite3
from sqlite3 import Error


class SQLiteCodesHelper:
    def __init__(self, db_file):
        """ Initialize the connection to the SQLite database. """
        self.db_file = db_file
        self.conn = None
        self.create_table()

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(f"Error connecting to database: {e}")

    def create_table(self):
        self.create_connection()
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS pc_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pc_code TEXT NOT NULL,
            model_name TEXT NOT NULL
        );
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_table_sql)
        except Error as e:
            print(f"Error creating table: {e}")
        self.close_connection()

    def insert_record(self, pc_code, model_name):
        self.create_connection()
        insert_sql = """
        INSERT INTO pc_codes (pc_code, model_name)
        VALUES (?,?);
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(insert_sql, (pc_code, model_name))
            self.conn.commit()
        except Error as e:
            print(f"Error inserting record: {e}")
        self.close_connection()

    def get_records(self):
        self.create_connection()
        select_sql = """SELECT pc_code FROM pc_codes;"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(select_sql)
            rows = cursor.fetchall()
            pc_codes = [row[0] for row in rows]
            return pc_codes
        except Error as e:
            print(f"Error retrieving records: {e}")
        self.close_connection()
        return []

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
