import sqlite3
from sqlite3 import Error

def create_connection(db_file):

        conn = None
        try:
                conn = sqlite3.connect(db_file)
        except Error as e:
                print(e)

        return conn

def select_all_images(conn):
        cur = conn.cursor()
        cur.execute("SELECT * FROM images")

        rows = cur.fetchall()

        for row in rows:
                print(row)

def main():
        database = "/home/adam/sci/db/image_paths.db"

        conn = create_connection(database)

        with conn:
                select_all_images(conn)

if __name__ == '__main__':
        main()
