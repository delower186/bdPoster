import mysql.connector
from database.db_util import format_keys, format_place_holders, format_values
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

# ------------------------------
# Generic update
# ------------------------------
def update(table, query, condition=None, value=None):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql = f"UPDATE {table} SET {query} {condition if condition else ''}"

        # Ensure value is tuple/list/dict
        if value is not None and not isinstance(value, (tuple, list, dict)):
            value = (value,)

        # Check if number of %s matches length of value
        placeholder_count = sql.count("%s")
        if placeholder_count != (len(value) if isinstance(value, (tuple, list)) else len(value.keys())):
            raise ValueError(f"Placeholder count {placeholder_count} does not match number of parameters {len(value)}")

        cur.execute(sql, value)
        conn.commit()
        cur.close()
        conn.close()
    except mysql.connector.Error as e:
        print("Update error:", e)

# ------------------------------
# Custom SQL update
# ------------------------------
def custom_update(table, custom_sql):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql = f"UPDATE {table} SET {custom_sql}"
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except mysql.connector.Error as e:
        print("Custom update error:", e)

# ------------------------------
# Select rows
# ------------------------------
def select(table, query, condition=None, value=None, limit=''):
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        sql = f"SELECT {query} FROM {table} {condition if condition else ''} {limit}"

        # 🔎 STRICT DEBUGGING (ADD HERE)
        if condition and "%s" in condition and value is None:
            raise ValueError(
                f"SQL has placeholders but no values provided → {sql}"
            )

        if value is not None:
            # Normalize single values
            if not isinstance(value, (tuple, list, dict)):
                value = (value,)
            cur.execute(sql, value)
        else:
            cur.execute(sql)

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows if rows else []

    except (mysql.connector.Error, ValueError) as e:
        print("Select error:", e)
        return []

# ------------------------------
# Delete row by id
# ------------------------------
def delete(table, value):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Ensure value is tuple
        if not isinstance(value, (tuple, list)):
            value = (value,)
        sql = f"DELETE FROM {table} WHERE id = %s"
        cur.execute(sql, value)
        conn.commit()
        cur.close()
        conn.close()
    except mysql.connector.Error as e:
        print("Delete error:", e)