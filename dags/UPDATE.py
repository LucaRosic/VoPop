import sqlite3

connection = sqlite3.connect("backend/db.sqlite3")
cursor = connection.cursor()
cursor.execute("UPDATE api_product_summary SET date = '2023-08-27 23:11:00.104619' WHERE product_id = 2" )
cursor.execute("DELETE from api_product_reviews WHERE date > '2023-08-27 T23:11:00.104619' AND product_id = 2" )
connection.commit()
cursor.close()