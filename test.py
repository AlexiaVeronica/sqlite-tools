import sqlite3
import typing


class SqliteOrm:

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
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

    def create_table(self, table_name, table_fields):

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

    def select(self, table_name, table_fields, where=None):

        sql = f"select * from {table_name}"

        if where:
            sql += f" where {where}"

        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        result = []

        for d in data:
            result.append(dict(zip(table_fields, d)))

        return result

    def update(self, table_name, table_fields, data, where=None):

        sql = f"update {table_name} set "

        for field in table_fields:
            sql += f"{field}=?,"

        sql = sql[:-1]

        if where:
            sql += f" where {where}"

        self.cursor.execute(sql, data)
        self.conn.commit()

    def delete(self, table_name, where=None):
        sql = f"delete from {table_name}"

        if where:
            sql += f" where {where}"

        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self


if __name__ == '__main__':
    sql = SqliteOrm("test.db")
    ins_list = [
        {"id": "1", "name": "张三", "age": 18},
        {"id": "2", "name": "李四", "age": 19},
        {"id": "3", "name": "王五", "age": 20},
        {"id": "4", "name": "赵六", "age": 21},
        {"id": "5", "name": "田七", "age": 22},
        {"id": "6", "name": "孙八", "age": 23},
        {"id": "7", "name": "周九", "age": 24},
        {"id": "8", "name": "吴十", "age": 25},
        {"id": "9", "name": "郑十一", "age": 26},
        {"id": "10", "name": "王十二", "age": 27},
    ]

    sql.create_table("test3", ins_list[0].keys())
    sql.insert_many("test3", ins_list)

    sql.insert("test3", {"id": "11", "name": "王十三", "age": 28})

