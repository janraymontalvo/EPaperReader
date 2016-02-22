import sqlite3
import getpass
import hashlib
import time

conn = sqlite3.connect('userAccounts.db') #ipath lang imong DB
c = conn.cursor()

'''
you have to close the db by adding these 3 codes

    conn.commit()
    c.close()
    conn.close()
    
Ibutang lang kung asa nimo ibutang
'''

class User:
    def __init__(self, ID, idnum, fname, lname, mname, userType, password, year):
        self.id = ID
        self.uname = idnum
        self.fname = fname
        self.lname = lname
        self.mname = mname
        self.userType = userType
        self.pword = password
        self.year = year



class Book:
    def __init__(self, ID, Title, Author, FilePath, Year):
        self.id = ID
        self.title = Title
        self.author = Author
        self.fpath = FilePath
        


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
        user = c.fetchone()
        return user
    else:
        return None
    ''' Return the an object User if the username and password information are correct, else return null '''


def ListBooks(username):
    c.execute("SELECT userType FROM userAccounts WHERE idnum=?", (username,))
    userType = c.fetchone()[0]
    if(userType==1):
        c.execute("SELECT year FROM userAccounts WHERE idnum=?", (username,))
        year = c.fetchone()[0]
        c.execute("SELECT * FROM Books WHERE year = ?", (year,))
    else:
        c.execute("SELECT * FROM Books")
    books = c.fetchall()
    return books
    ''' Return an array of objects Book allowed for username, else return null '''

def main():
    # test = ListBooks(11100346)
    # print(test)
    # time = Today()
    # print(time)
    test = LogIn(11100346, "churvaloo")
    print (test)
    
    conn.commit()
    c.close()
    conn.close()

main()
