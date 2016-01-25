#!/usr/bin/python
#from PIL import Image, ImageDraw, ImageFont
# get an image
# base = Image.open('taylor.jpg').convert('RGBA')

# # make a blank image for the text, initialized to transparent text color
# txt = Image.new('RGBA', base.size, (255,255,255,0))

# # get a font
# fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
# # get a drawing context
# d = ImageDraw.Draw(txt)

# # draw text, half opacity
# d.text((10,10), "Hello", font=fnt, fill=(255,255,255,128))
# # draw text, full opacity
# d.text((10,60), "World", font=fnt, fill=(255,255,255,255))

# out = Image.alpha_composite(base, txt)

# out.show()

# Load the database
import sqlite3
conn = sqlite3.connect('Accounts.db')
c = conn.cursor() # use c.execute() to execute statements and c.commit() to commit changes
# Attemp log in
data = c.execute('SELECT * FROM users WHERE idnum=111')
