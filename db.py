import sqlite3
import getpass
import hashlib

conn = sqlite3.connect('../sqlite/userAccounts.db')
c = conn.cursor()

def db_LogIn(username, password):
	flag=0;
	temp_user = raw_input("Enter idnum: ")
	c.execute("SELECT idnum FROM userAccounts")
	for row in c.fetchall():
		if temp_user == row[0]:
			flag = 1
	if(flag!=1):	
		print "idnum does not exist!"
		return 0
	temp_pass = hashlib.sha224(getpass.getpass("Enter Password: ")).hexdigest()
	#checkpass = 
	c.execute("SELECT password FROM userAccounts WHERE idnum=?", (temp_user,))
	checkpass = c.fetchone()
	x = len(str(checkpass))-3
	#print str(checkpass)
	if str(temp_pass) == checkpass[0]:
		print "PASSWORD SUCCESFFUL!"
		c.execute("SELECT userType,year, idnum FROM userAccounts WHERE idnum=?", (temp_user,))
		uTypeYearID = c.fetchone()
		if uTypeYearID[0]==1:
			studentView(uTypeYearID[1],uTypeYearID[2])
		elif uTypeYearID[0]==2:
			teacherView()
		elif uTypeYearID[0]==3:
			adminView()
	else:
		print "WRONG PASSWORD"

def adminView():
	choice = 0
	while(choice!=2):
		c.execute("SELECT Title, Author FROM Books")
		data = c.fetchall()
		choice = input("1 - Open Book\n2 - Logout\n")
		if(choice==1):
			for idx, books in enumerate(data):
				print(str(idx+1)+"-" + books[0]+" by "+books[1])
				idx+=1
			print "0 - Go Back"
			book_choice = input("Open book number: ")
			if(book_choice==0):
				continue
			else:
				c.execute("SELECT FilePath FROM Books WHERE ID=?", (book_choice,))
				path = c.fetchone()
				print("Opening " + path[0])
		else:
			return 0
def teacherView():
	choice = 0
	while(choice!=3):
		c.execute("SELECT Title, Author FROM Books")
		data = c.fetchall()
		choice = input("1- Open Book\n2- Reset a Student's Password\n3-LogOut\n")
		if(choice==1):
			for idx, books in enumerate(data):
				print(str(idx+1)+"-" + books[0]+" by "+books[1])
				idx+=1
			print "0 - Go Back"
			book_choice = input("Open book number: ")
			if(book_choice==0):
				continue
			else:	
				c.execute("SELECT FilePath FROM Books WHERE ID=?", (book_choice,))
				path = c.fetchone()
				print("Opening " + path[0])
		elif(choice==2):
			student_id = raw_input("Enter a student id")
			c.execute("UPDATE userAccounts SET password=? WHERE idnum=?", (hashlib.sha224("00000").hexdigest(),student_id,))
		else:
			return 0

def studentView(year, idnum):
	idx=0
	choice = 0
	c.execute("SELECT Title,Author FROM Books WHERE year=?", (year,))
	data = c.fetchall()
	while(choice!=4):
		choice = input("1 - Open Book \n2 - Change password\n3 - Logout\n")
		if (choice==1):
			for idx,books in enumerate(data):
				print(str(idx+1)+"-" +books[0]+" by "+books[1])
				idx+=1
			print "0 - Go Back"
			book_choice = input("Enter book number: ")
			if(book_choice==0):
				continue
			else:	
				c.execute("SELECT FilePath FROM Books WHERE Year=? LIMIT ?,?", (year, book_choice-1,book_choice-1))
				path = c.fetchone()
				print ("Opening " + path[0])
		elif choice==2:
			c.execute("SELECT password FROM userAccounts WHERE idnum=?", (idnum,))
			password = c.fetchone()[0]
			curr = hashlib.sha224(getpass.getpass("Enter current Password: ")).hexdigest()
			if(password == curr):
				new = getpass.getpass("Enter new password: ")
				conf = getpass.getpass("Confirm password: ")
				if(new==conf):
					new = hashlib.sha224(new).hexdigest()
					c.execute("UPDATE userAccounts SET password=? WHERE idnum=?", (new,idnum,))
					conn.commit()
					print "SUCCESSFUL!"
			else:
				print "WRONG PASSWORD!"
		else:
			return 0
	
def Register():
	flag=0
	c.execute("SELECT idnum FROM userAccounts")
	idnum = raw_input("Enter id number: ")
	for row in c.fetchall():
		if str(idnum) == row[0]:
			flag = 1
	if(flag==1):	
		print "idnum is already taken!"
		return 0
	fname = raw_input("Enter first name: ")
	lname = raw_input("Enter last name: ")
	mname = raw_input("Enter middle name: ")
	userType = input("Enter Usertype \n1-Student \n2-Teacher\n3-Admin: ")
	password = hashlib.sha224(getpass.getpass("Enter Password: ")).hexdigest()
	if userType==1:
		year = raw_input("Enter current year (Number only)")
	else:
		year = None
	c.execute("INSERT INTO userAccounts (idnum,fname,lname,mname,userType, password, year) VALUES (?,?,?,?,?,?,?)", (str(idnum), str(fname), str(lname), str(mname), userType, password,year))
	conn.commit()

def LogIn():
	flag=0;
	temp_user = raw_input("Enter idnum: ")
	c.execute("SELECT idnum FROM userAccounts")
	for row in c.fetchall():
		if temp_user == row[0]:
			flag = 1
	if(flag!=1):	
		print "idnum does not exist!"
		return 0
	temp_pass = hashlib.sha224(getpass.getpass("Enter Password: ")).hexdigest()
	#checkpass = 
	c.execute("SELECT password FROM userAccounts WHERE idnum=?", (temp_user,))
	checkpass = c.fetchone()
	x = len(str(checkpass))-3
	#print str(checkpass)
	if str(temp_pass) == checkpass[0]:
		print "PASSWORD SUCCESFFUL!"
		c.execute("SELECT userType,year, idnum FROM userAccounts WHERE idnum=?", (temp_user,))
		uTypeYearID = c.fetchone()
		if uTypeYearID[0]==1:
			studentView(uTypeYearID[1],uTypeYearID[2])
		elif uTypeYearID[0]==2:
			teacherView()
		elif uTypeYearID[0]==3:
			adminView()
	else:
		print "WRONG PASSWORD"


def main():
	choice=0
	while(choice!=3):
		choice = input("Enter your choice:\n1-Register\n2-Log In\n3-Exit\n")
		if(choice==1):
			Register()
		elif(choice==2):
			LogIn()
		elif(choice>3):
			print "INVALID CHOICE!"

	conn.commit()
	c.close()
	conn.close()

main()