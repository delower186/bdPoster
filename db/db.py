import mysql.connector
from db.db_util import format_keys, format_place_holders, format_values
# ------------------------------
# MySQL connection
# ------------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="192.168.88.230",
        port=3306,
        user="postauto",
        password='ik5129!-CVr(n"97_5NB0Ett#hpIM',
        database="post_automator",
        autocommit=True,
        use_pure=True,  # <-- Important
        auth_plugin="mysql_native_password"
    )

# ------------------------------
# Generic insert
# ------------------------------
def insert(table, data):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql = f"INSERT INTO {table} ({format_keys(data)}) VALUES ({format_place_holders(data)})"
        cur.execute(sql, format_values(data))
        conn.commit()
        last_id = cur.lastrowid
        cur.close()
        conn.close()
        return last_id
    except mysql.connector.Error as e:
        print("Insert error:", e)