# database.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="llpekgwy_administrador",
        password="*F5g@^^{.246",
        database="llpekgwy_quehaypahacer",
        port=3306
    )