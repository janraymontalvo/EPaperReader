import sqlite3
import getpass
import hashlib
import time

conn = sqlite3.connect('../sqlite/userAccounts.db') #ipath lang imong DB
c = conn.cursor()

'''
you have to close the db by adding these 3 codes

    conn.commit()
    c.close()
    conn.close()
    
Ibutang lang kung asa nimo ibutang
'''

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
    



    ''' Return the an object User if the username and password information are correct, else return null '''



    ''' Return an array of objects Book allowed for username, else return null '''

def main():
    test = ListBooks(11100346)
    print(test)
    time = Today()
    print(time)
    test = LogIn(11100346, "00000")
    print (type(test))
    print test.uname
    conn.commit()
    c.close()
    conn.close()

main()
