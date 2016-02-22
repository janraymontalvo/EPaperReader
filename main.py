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


keys =  [
		['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
		['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',' J'],
		['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'],
		['U', 'V', 'W', 'X', 'Y', 'Z', ' ', 127, 0, 0]
		]
		#DEL = 127, 0 = OK
prebase = None
base = None
lastkey = ''


def ShowKeyboard():
	global base, prebase,lastkey
	prebase = base
	keyboard = Image.open('resources/ui/keyboard.png').convert('RGBA')
	base.paste(keyboard, (0, 560), keyboard)
	curr_selection = 
	curr_region = 

	# Loop: Get button input
	# Get selection and region and invert color 


def HideKeyboard():
	base = prebase
	prebase = None

def Main():
	# Draw the log in screen
	global base, lastkey
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
	base.show()
	base.save('cache/screens/screen.png', "PNG")

	# Code for drawing text on image
	txt = Image.new('RGBA', base.size, (255,255,255,0))
	fnt = ImageFont.truetype('resources/fonts/ACaslonPro-Regular.otf', 35)

	ShowKeyboard()
	base.show()
	base.save('cache/screens/screen.png', "PNG")

	# # Get input for Log in
	# username = ''
	# x = 80
	# while True:
	# 	key = raw_input("ID: ") # Wait for button input. Substitute for on-screen keyboardbutton!!
	# 	if key.strip() == 'done':
	# 		break
	# 	username += key
	# 	d = ImageDraw.Draw(txt)
	# 	d.text((x,239), key.strip(), font=fnt, fill=(0,0,0,255))
	# 	base = Image.alpha_composite(base, txt)
	# 	x += 20
	# 	base.show()
	# 	# base.save('cache/screens/screen.png', "PNG")
		
	# print username

	# # Get input for password
	# password = ''
	# x = 80
	# while True:
	# 	key = raw_input("Pass: ") # Same as above
	# 	if key.strip() == 'done':
	# 		break
	# 	password += key
	# 	d = ImageDraw.Draw(txt)
	# 	d.text((x,345), "* " * len(key.strip()), font=fnt, fill=(0,0,0,255))
	# 	base = Image.alpha_composite(base, txt)
	# 	x += 20
	# 	base.show()
	# 	# base.save('cache/screens/screen.png', "PNG")

	# print password

	# # Attemp log in
	

	# base.show()
	# # base.save('cache/screens/screen.png', "PNG")


if __name__ == '__main__':
    Main()