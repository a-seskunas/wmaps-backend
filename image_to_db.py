import sqlite3
from sqlite3 import Error


def create_connection(db_file):
	conn = None
	try:
		con = sqlite3.connect(db_file)
	except Error as e:
		print(e)

	return conn

def create_image(conn, image):
	sql = '''INSERT INTO images(path, date, z, region, image_name) VALUES(?,?,?,?,?)'''
	cur = conn.cursor()
	cur.execute(sql, image)
	conn.commit()
	return cur.lastrowid

