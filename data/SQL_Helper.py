import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'app',
    'password': 'pass',
    'database': 'app'
}

class SQLHelper:
    @staticmethod
    def get_conn():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except Error as e:
            print(f"Ошибка подключения к БД: {e}")
            raise

    @staticmethod
    def get_status_payment():

        conn = None
        cursor = None
        try:
            conn = SQLHelper.get_conn()
            cursor = conn.cursor()
            # ScalarHandler<String> аналогичен fetchone()[0]
            sql = "SELECT status FROM payment_entity ORDER BY created DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    @staticmethod
    def get_amount_payment():

        conn = None
        cursor = None
        try:
            conn = SQLHelper.get_conn()
            cursor = conn.cursor()
            sql = "SELECT amount FROM payment_entity WHERE status = 'APPROVED' ORDER BY created DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            return int(result[0]) if result else 0
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    @staticmethod
    def get_status_credit():
        conn = None
        cursor = None
        try:
            conn = SQLHelper.get_conn()
            cursor = conn.cursor()
            sql = "SELECT status FROM credit_request_entity ORDER BY created DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
