import mysql.connector
from mysql.connector import Error

def test_mysql_connection():
    try:
        # sesuaikan host, user, dan password dengan konfigurasi lokal
        connection = mysql.connector.connect(
            host='localhost',
            database='python_db',
            user='root',
            password=''
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"berhasil terhubung ke server MySql versi: {db_info}")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"connected to database: {record}")
    
    except Error as e:
        print(f"gagal terhubung ke database: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Koneksi MySql ditutup.");

if __name__ == '__main__':
    test_mysql_connection()