import mysql.connector
import ast

try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="BANK"
    )
    mycursor = db.cursor()
except mysql.connector.Error as e:
    print(f"Error connecting to database: {e}")
    sys.exit()