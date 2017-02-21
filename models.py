import sqlite3 as sql
import hashlib


def insert_user(username, password):

    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute('INSERT INTO Users VALUES (default,?,?)', username, password)
    con.commit()
    con.close()


def load_user(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT username from users where username = (?)", [id])
    userrow = cur.fetchone()
    userid = userrow[0]  # or whatever the index position is
    return userid


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
    t = (username,)
    cur.execute("SELECT password FROM users WHERE username =?", t)
    password = cur.fetchone()
    con.close()
    return password[0]


def md5sum(t):
    return hashlib.md5(t).hexdigest()
