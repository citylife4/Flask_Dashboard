import sqlite3 as sql


def insert_user(user_id, username, password):
    """

    :type password: String
    :param password:
    :param user_id:
    :type username: String
    """
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute('INSERT INTO Users VALUES (?,?)', username, password)
    con.commit()
    con.close()


def retrieve_users():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM users")
    users = cur.fetchall()
    con.close()
    return users


def get_password(username):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT password FROM users WHERE username =?", (username) )
    password = cur.fetchall()
    con.close()
    return password
