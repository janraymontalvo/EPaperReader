#!/usr/bin/python
## Main module for EPaperReader Application
#TODO: (db) - indicates database operations, (hw) - hardware operations
# -Launch procedure (Splash screen, log in screen)
# -Load accounts database (db)
# -User log in (db)
# -Load keyboard
# -Log in procedure (db)
# -Save session (db)
# -Load books database (db)
# -Openepubs
# -Book navigation
# -Learning (db)
# -Checking and storing learning exercises (db)
# 
# -Load system time
# -Load battery life (hw) 
# -Read input buttons (hw) (interrupt)

from PIL import Image, ImageDraw, ImageFont
import sqlite3

def main():
	# Draw the log in screen
	base = Image.open('resources/ui/epd.png').convert('RGBA')
	temp_im = Image.open('resources/ui/label_title.png')
	base.paste(temp_im, (95,40), temp_im)
	temp_im = Image.open('resources/ui/label_login.png')
	base.paste(temp_im, (190,135), temp_im)
	temp_im = Image.open('resources/ui/label_id.png')
	base.paste(temp_im, (220,200), temp_im)
	temp_im = Image.open('resources/ui/element_textbox.png')
	base.paste(temp_im, (71,231), temp_im)
	base.paste(temp_im, (71,331), temp_im)
	temp_im = Image.open('resources/ui/label_password.png')
	base.paste(temp_im, (184,300), temp_im)
	base.save('cache/screens/screen.png', "PNG")

	# Code for drawing text on image
	txt = Image.new('RGBA', base.size, (255,255,255,0))
	fnt = ImageFont.truetype('resources/fonts/Inconsolata-Regular.ttf', 36)


	# Load the database
	conn = sqlite3.connect('Accounts.db')
	c = conn.cursor() # use c.execute() to execute statements and c.commit() to commit changes

	# Get input for Log in
	username = ''
	x = 77
	while True:
		key = raw_input("ID: ") # Wait for button input. Substitute for on-screen keyboardbutton!!
		if key.strip() == 'done':
			break
		username += key
		d = ImageDraw.Draw(txt)
		d.text((x,235), key.strip(), font=fnt, fill=(0,0,0,255))
		base = Image.alpha_composite(base, txt)
		x += 20
		base.save('cache/screens/screen.png', "PNG")
		
	print username

	# Get input for password
	password = ''
	x = 77
	while True:
		key = raw_input("Pass: ") # Same as above
		if key.strip() == 'done':
			break
		password += key
		d = ImageDraw.Draw(txt)
		d.text((x,335), key.strip(), font=fnt, fill=(0,0,0,255))
		base = Image.alpha_composite(base, txt)
		x += 20
		base.save('cache/screens/screen.png', "PNG")

	# Attemp log in
	print c.execute('SELECT idnum, password WHERE ')

	conn.close()
	base.save('cache/screens/screen.png', "PNG")


if __name__ == '__main__':
    main()