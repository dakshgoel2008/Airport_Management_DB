import pymysql

def get_connection(user: str, password: str, db: str = None) -> pymysql.connections.Connection:
    return pymysql.connect(
        host="localhost",
        port=3306,
        user=user,
        password=password,
        db=db,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )