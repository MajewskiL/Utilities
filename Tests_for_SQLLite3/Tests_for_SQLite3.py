import sqlite3
import os


class SQLite3Test:

    """It's recommended to keep the sequence:
    1. Create object SQLite3Check
    2. Check is file exists
    3. Establish connection
    4. Check is table exists
    5. Check are columns exists
    6. Do the rest of tests on tables: is column primary key, not null

    To do tests: is unique and is foreign key"""

    cursor_message = f"There is no cursor to connection."  # Is it proper message?
    no_table_message = f"There is no table you are looking for."

    def __init__(self, file_name):  # file_name -> string
        self.file_name = file_name
        self.conn = None
        self.cursor = None

    def is_file_exist(self):
        if not os.path.exists(self.file_name):
            return f"The file '{self.file_name}' does not exist or is outside of the script directory."
        return False

    def connect(self):
        ans = self.is_file_exist()
        if ans:
            return ans
        try:
            self.conn = sqlite3.connect(self.file_name)
            self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as err:
            return f"DataBase {self.file_name} may be locked. An error was returned when trying to connect: {err}."

    def close(self):
        try:
            self.conn.close()
        except AttributeError:
            return self.cursor_message

    def run_query(self, query):
        try:
            lines = self.cursor.execute(f"{query}")
        except AttributeError:
            return self.cursor_message
        except sqlite3.OperationalError as err:
            self.close()
            return f"Error '{err}' occurred while trying to read from database '{self.file_name}'."
        except sqlite3.DatabaseError as err:
            self.close()
            return f"Error '{err}' occurred while trying to read from database '{self.file_name}'."
        return lines

    def is_table_exist(self, name):  # table name -> string
        lines = self.run_query(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{name}';").fetchall()
        if lines[0][0] == 0:
            self.close()
            return f"There is no table named '{name}' in database {self.file_name}"

    def number_of_records(self, name, expected_lines):   # table name -> string, expected_lines -> integer
        lines = self.run_query(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        if lines != expected_lines:
            self.close()
            return f"Wrong number of records in table {name}. Expected {expected_lines}, found {lines}"

    def is_column_exist(self, name, names):  # table name -> string, column names -> list of strings for all columns, or list with one string for one column
        lines = self.run_query(f'select * from {name}').description
        if len(names) != 1:
            if sorted(names) != sorted([line[0] for line in lines]):
                self.close()
                return f"There is something wrong in table {name}. Found column names: {[line[0] for line in lines]}. Expected {names}'"
        else:
            if not any([names[0] == c_name for c_name in [line[0] for line in lines]]):
                self.close()
                return f"There is something wrong in table {name}. Found column names: {[line[0] for line in lines]}. Expected to find '{names[0]}'"

    def table_info(self, name, column, attribute):   # table name -> string, column name -> string, attr ("PK" Primary Key; "NN" Not null)
        lines = self.run_query(f"PRAGMA table_info({name})").fetchall()
        if column not in [line[1] for line in lines]:
            return f"There is no column {column}."
        for line in lines:
            if attribute == "PK":
                if line[1] == column and line[5] != 1:
                    self.close()
                    return f"There is no PRIMARY KEY parameter in {name} on column {column}."
            elif attribute == "NN":
                if line[1] == column and line[3] != 1:
                    return f"There is no NOT NULL parameter in {name} on column {column}."

    def is_unique(self, name, column):  # table name -> string, column name -> string
        lines = self.run_query(f"SELECT inf.name FROM pragma_index_list('{name}') as lst, pragma_index_info(lst.name) as inf WHERE lst.[unique] = 1;").fetchall()
        if not any([column in line for line in lines]):
            return f"There is no UNIQUE parameter in {name} on column {column}."
        return True

    def is_foreign_key(self, name, column):  # table name -> string, column name -> string
        lines = self.run_query(f"SELECT * FROM pragma_foreign_key_list('{name}');").fetchall()
        if not any([column in line for line in lines]):
            return f"There is no FOREIGN KEY parameter in {name} on column {column}."
        return True

a = SQLite3Test("data..db")
print(a.connect())
print(a.run_query("SELECT * FROM ham"))
