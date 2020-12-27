import sqlite3


def conn():
    try:
        return sqlite3.connect('example.db')
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def execute(_conn, sql, param):
    try:
        c = _conn.cursor()
        c.execute(sql, param)
        _conn.commit()
    except Exception as ex:
        print("exception is: " + str(ex))


def select(_conn, sql, param):
    try:
        c = _conn.cursor()
        c.execute(sql, param)
        result = c.fetchone()
        return result
    except Exception as ex:
        print("exception is: " + str(ex))


def many(_conn, sql, param):
    try:
        c = _conn.cursor()
        c.execute(sql, param)
        result = c.fetchall()
        return result
    except Exception as ex:
        print("exception is: " + str(ex))


def close(_conn):
    try:
        _conn.close()
    except Exception as ex:
        print("exception is: " + str(ex))
