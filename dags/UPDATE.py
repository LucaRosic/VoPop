import sqlite3

connection = sqlite3.connect("backend/db.sqlite3")
cursor = connection.cursor()
cursor.execute("UPDATE api_product_summary SET date = '2024-06-27 23:11:00.104619' WHERE product_id = 4" )
connection.commit()
result = cursor.execute("DELETE FROM api_product_reviews WHERE date > '2024-06-27' AND product_id = 4" )
connection.commit()
cursor.close()