"""
database.py - connects our Python (tkinter) app to MySQL.

Install the connector first (run this in your terminal):
    pip install mysql-connector-python
"""

import mysql.connector

# ---------------------------------------------------------------
# STEP 1: Change these to match YOUR MySQL setup
# ---------------------------------------------------------------
HOST = "localhost"
USER = "root"
PASSWORD = ""   # <- put your own password here
DATABASE = "placement_tracker"     # <- the database you created in MySQL
# (Don't push your real password to GitHub!)


# ---------------------------------------------------------------
# STEP 2: Connecting to the database
# ---------------------------------------------------------------
def connect():
    """Opens a connection to MySQL and returns it."""
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
    )
    return connection


# ---------------------------------------------------------------
# STEP 3: Getting data  (use for SELECT queries)
# ---------------------------------------------------------------
def get_all(query, values=()):
    """
    Runs a SELECT query and returns ALL matching rows as a list.
    Each row is a dictionary, e.g. row["name"]

    Example:
        students = get_all("SELECT * FROM students")
        cse = get_all("SELECT * FROM students WHERE branch = %s", ("CSE",))
    """
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(query, values)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows


def get_one(query, values=()):
    """
    Runs a SELECT query and returns just ONE row (or None if nothing found).

    Example:
        student = get_one("SELECT * FROM students WHERE id = %s", (5,))
    """
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(query, values)
    row = cursor.fetchone()

    cursor.close()
    connection.close()
    return row


# ---------------------------------------------------------------
# STEP 4: Changing data  (use for INSERT, UPDATE, DELETE)
# ---------------------------------------------------------------
def run(query, values=()):
    """
    Runs an INSERT, UPDATE or DELETE query and saves the change.
    Returns True if it worked, False if something went wrong.

    Example:
        run("INSERT INTO companies (name, ctc) VALUES (%s, %s)", ("TCS", 7.0))
        run("DELETE FROM companies WHERE id = %s", (3,))
    """
    try:
        connection = connect()
        cursor = connection.cursor()

        cursor.execute(query, values)
        connection.commit()      # <- this actually saves the change

        cursor.close()
        connection.close()
        return True

    except mysql.connector.Error as error:
        print("Database error:", error)
        return False


# ---------------------------------------------------------------
# Run this file directly to check your connection works:
#     python database.py
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        connect().close()
        print("Connected to MySQL successfully!")
    except mysql.connector.Error as error:
        print("Could not connect:", error)