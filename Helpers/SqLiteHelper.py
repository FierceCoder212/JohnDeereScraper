import sqlite3
from sqlite3 import Error


class SQLiteHelper:
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
        CREATE TABLE IF NOT EXISTS section_diagrams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section_diagram TEXT NOT NULL,
            section_diagram_url TEXT
        );
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_table_sql)
        except Error as e:
            print(f"Error creating table: {e}")
        self.close_connection()

    def insert_record(self, section_diagram, section_diagram_url):
        insert_sql = """
        INSERT INTO section_diagrams (section_diagram, section_diagram_url)
        VALUES (?, ?);
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(insert_sql, (section_diagram, section_diagram_url))
            self.conn.commit()
        except Error as e:
            print(f"Error inserting record: {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
