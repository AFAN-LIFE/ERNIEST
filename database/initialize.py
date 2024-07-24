from database.connection import gpt_connection

def initialize_database():
    print('初始化数据库')
    tables_to_check = ['conversations', 'messages']
    # 创建游标对象
    cursor = gpt_connection.cursor()
    # 存储已存在的表名
    existing_tables = []
    # 查询数据库中已有的表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in cursor.fetchall():
        existing_tables.append(table['name'].lower())
    # 检查并创建表
    for table in tables_to_check:
        if table not in existing_tables:
            if table.lower() == 'conversations':
                cursor.execute("""
                    CREATE TABLE conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT NOT NULL,
                        start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        end_time TIMESTAMP,
                        theme TEXT,
                        is_deleted BOOLEAN DEFAULT 0
                    );
                """)
                print(f"Table {table} created.")
            elif table.lower() == 'messages':
                cursor.execute("""
                    CREATE TABLE messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        conversation_id INTEGER,
                        sender TEXT NOT NULL,
                        message TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_deleted BOOLEAN DEFAULT 0,
                        FOREIGN KEY (conversation_id) REFERENCES Conversations(id)
                    );
                """)
                print(f"Table {table} created.")
        else:
            print(f"Table {table} already exists.")
    # 提交更改
    gpt_connection.commit()
    # 关闭连接
    cursor.close()

if __name__ == '__main__':
    initialize_database()