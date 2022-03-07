import MySQLdb
import base64 

db = MySQLdb.connect(host="localhost",
		     user="root",
		     passwd="skoony78",
		     db="charts")

cur = db.cursor()

#with open('/root/sci/new_testy.png', 'rb') as image:
	#imager = image.read()

image = open('/root/sci/new_testy.png', 'rb').read()
sql = "INSERT INTO images(idpic,caption,img) VALUES(12,2010,%s)"

cur.execute(sql, (image,))
#cur.commit()

sql = "SELECT * from images"
cur.execute(sql)
data = cur.fetchall()

#im = base64.b64decode(data[0][0])
print type(data[0][0])

f = open('/var/www/html/images/new_testy.png', 'wb')
f.write(data[0][0].decode('base64'))
f.close()

cur.close()
db.close()
