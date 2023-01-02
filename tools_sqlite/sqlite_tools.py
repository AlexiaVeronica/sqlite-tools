import sqlite3
import typing
import pandas as pd


class SqliteTools:

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def sort_table_values(self, table_name: str, table_fields: dict) -> list:
        data = []
        for table_name in self.table_fields(table_name):
            value = table_fields.get(table_name)
            if isinstance(value, dict):
                value = str(value)
            if isinstance(value, list):
                value = str(value)
            data.append(value)
        return data

    def table_fields(self, table_name):
        return [i[1] for i in self.cursor.execute(f"PRAGMA table_info({table_name})")]

    def create_table(self, table_name: str, table_fields):
        sql = f"create table if not exists {table_name} ("
        for field in table_fields:
            if field == "id":  # 如果是id字段则设置为主键
                sql += f"{field} TEXT PRIMARY KEY,"
            else:
                sql += f"{field} TEXT,"
        sql = sql[:-1] + ")"

        self.cursor.execute(sql)
        self.conn.commit()

    def insert(self, table_name, table_fields: dict):
        sql = f"insert into {table_name} values ("
        for field in table_fields.keys():
            sql += "?,"

        sql = sql[:-1] + ")"
        # 获取数据库列名称
        try:
            self.cursor.execute(sql, self.sort_table_values(table_name, table_fields))
        except sqlite3.IntegrityError as e:
            print("主键冲突:", e)
        self.conn.commit()

    def insert_many(self, table_name, data: typing.List[dict]):
        sql = f"insert into {table_name} values ("

        for field in self.table_fields(table_name):
            sql += "?,"
        sql = sql[:-1] + ")"

        data_list = []
        for table_fields in data:
            data_list.append(self.sort_table_values(table_name, table_fields))

        self.cursor.executemany(sql, data_list)
        self.conn.commit()

    def insert_and_update(self, table_name, table_fields: dict):
        sql = f"insert or replace into {table_name} values ("

        for field in table_fields.keys():
            sql += "?,"
        sql = sql[:-1] + ")"

        try:
            self.cursor.execute(sql, self.sort_table_values(table_name, table_fields))
        except sqlite3.IntegrityError as e:
            print("主键冲突:", e)
        self.conn.commit()

    def select(self, table_name, values: dict = None, where=None):
        sql = f"select * from {table_name}"
        if where:
            sql += f" where {where}"
        if values:
            if values.get("order"):
                sql += f" order by {values.get('order')}"
            if values.get("limit"):
                sql += f" limit {values['limit']}"
            if values.get("offset"):
                sql += f" offset {values['offset']}"

        return pd.read_sql_query(sql, self.conn).to_dict(orient="records", into=dict)

    def update(self, table_name, update_fields: dict, where: dict):
        sql = f"update {table_name} set "
        for field in update_fields.keys():
            sql += f"{field} = '{update_fields[field]}',"
        sql = sql[:-1]
        # sql += f" where {where}"
        for field in where.keys():
            sql += f" where {field} = {where[field]}"
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def delete(self, table_name, where=None):
        sql = f"delete from {table_name} "

        if where:
            sql += f"where {where}"

        self.cursor.execute(sql)
        self.conn.commit()

    def get(self, table_name, key_value):
        where = f"id={key_value}"
        try:
            return self.select(table_name, None, where)[0]
        except IndexError:
            return None

    def close(self):
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self
