import tools_sqlite

if __name__ == '__main__':
    sql = tools_sqlite.SqliteTools("test.db")
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
    data = {"id": "8888", "name": "十三", "age": 777}
    were = {"id": "11"}
    sql.update("test3", data, were)
    sql.insert("test2", {"id": "666", "name": {"id": "8888", "name": "十三", "age": 777}, "age": 28})
    print(sql.select("test2", {"id": 666, }, {"limit": "3"}))
