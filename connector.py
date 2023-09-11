import mysql.connector


def connect():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="equationevo"
    )
    return db_connection
