
import psycopg2

connection = psycopg2.connect(database="airflow", user='airflow', password='airflow', host='localhost', port= '5432')
cursor = connection.cursor()


cursor.execute("UPDATE api_product_summary SET date = '2024-03-27 23:11:00.104619' WHERE product_id = 1" )
connection.commit()
result = cursor.execute("DELETE FROM api_product_reviews WHERE date > '2024-03-27' AND product_id = 1" )
connection.commit()

result = cursor.execute('SELECT * FROM api_product_reviews')
print(cursor.fetchall())
cursor.close()