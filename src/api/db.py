import sqlite3
from typing import List, Tuple


class Db:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def create_table(self, table_name: str, fields: list) -> None:
        fields_str = ", ".join(fields)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({fields_str})")

    def insert(self, table_name: str, data: dict) -> None:
        columns_str = ", ".join(data.keys())
        values_str = ", ".join([f"'{value}'" for value in data.values()])
        self.cursor.execute(
            f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"
        )
        self.conn.commit()

    def select(
        self, table_name: str, columns: list = None, condition: str = None
    ) -> list:
        if columns:
            columns_str = ", ".join(columns)
        else:
            columns_str = "*"

        if condition:
            self.cursor.execute(
                f"SELECT {columns_str} FROM {table_name} WHERE {condition}"
            )
        else:
            self.cursor.execute(f"SELECT {columns_str} FROM {table_name}")

        all_tuples = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        return [dict(zip(columns, row)) for row in all_tuples]

    def update(self, table_name: str, data: dict, condition: str) -> None:
        set_str = ", ".join([f"{column}='{value}'" for column, value in data.items()])
        self.cursor.execute(f"UPDATE {table_name} SET {set_str} WHERE {condition}")
        self.conn.commit()

    def delete(self, table_name: str, condition: str) -> None:
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
        self.conn.commit()
