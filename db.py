import sqlite3
import getpass
import hashlib
import time

conn = sqlite3.connect('userAccounts.db')
c = conn.cursor()


class User:
    def __init__(self, idnum, fname, lname, mname, userType, year):
        self.uname = idnum
        self.fname = fname
        self.lname = lname
        self.mname = mname
        self.userType = userType
        self.year = year


class Book:
    def __init__(self, Title, Author, FilePath, Year):
        self.title = Title
        self.author = Author
        self.fpath = FilePath
        self.year = Year


def Today():
    ''' Return the current date and time as string in the format mm/dd/yyyy hh:mm AM/PM '''
    dateandtime = time.strftime("%m/%d/%Y %I:%M:%S %p")
    return dateandtime


def LogIn(username, password):
    newpassword = hashlib.sha224(password).hexdigest()
    c.execute("SELECT password FROM userAccounts WHERE idnum=?", (username,))
    checkpass = c.fetchone()[0]
    if(newpassword == checkpass):
        c.execute("SELECT * FROM userAccounts WHERE idnum=?", (username,))
        output = c.fetchone()
        user = User(output[1], output[2], output[3], output[4], output[5], output[7])
        return user
    else:
        return None


def ListBooks(username):
    c.execute("SELECT userType FROM userAccounts WHERE idnum=?", (username,))
    userType = c.fetchone()[0]
    if(userType==1):
        c.execute("SELECT year FROM userAccounts WHERE idnum=?", (username,))
        year = c.fetchone()[0]
        c.execute("SELECT * FROM Books WHERE year = ?", (year,))
    else:
        c.execute("SELECT * FROM Books")
    output = c.fetchall()

    books = []
    for i in output:
    	books.append(Book(i[1], i[2], i[3], i[4]))
    return books
