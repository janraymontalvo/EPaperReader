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

import argparse
import PIL.ImageOps
from PIL import Image, ImageDraw, ImageFont
import db
import epub

#Parse args
parser = argparse.ArgumentParser()
parser.add_argument("--pi", 
                    help="Execute the script on the Raspberry Pi.")
parser.add_argument("--not-pi",
                    action="store_true",
                    help="Execute the script on a non-Raspberry Pi computer.")
args = parser.parse_args()
if not (args.pi or args.not_pi):
    parser.print_help()
    parser.error('No parameter given.')

if args.pi:
    import epd


keys =  [ #DEL = 127, 0 = OK
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
        ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'],
        ['U', 'V', 'W', 'X', 'Y', 'Z', ' ', 127, 0, 0]]
base, user, books = None, None, None
p_flag = False
pressed = ''
textbuffer = ''
crsr = [83, 286] # Cursor for text input from keyboard


def UpdateDisplay():
    ''' Update the EPD screen '''
    base.save('cache/screens/screen.png', "PNG")
    tinyfnt = ImageFont.truetype('resources/fonts/OpenSans-Regular.ttf', 18)
    now = db.Today()
    temp_im = Image.open('resources/ui/element_status_bar.png')
    base.paste(temp_im, (0,0))
    draw = ImageDraw.Draw(base)
    draw.text((265, 2), now, fill=(0,0,0), font=tinyfnt)
    if args.not_pi:
        base.show()
    
    if args.pi:
        epd.update_screen(base)
    

def GetInput():
    ''' Get input from keyboard or GPIO buttons '''
    if args.not_pi:
        inp = raw_input("Input: ") #Change this to button input'
        return inp.strip()
    
    if args.pi:
        inp = epd.button_press()
        return inp


def ShowKeyboard():
    ''' Keyboard '''
    global base, pressed, textbuffer
    textbuffer = ''
    keyboard = Image.open('resources/ui/keyboard.png').convert('RGB')
    base.paste(keyboard, (0, 560))
    
    #Select '0'
    letter = [0, 0] # Corresponds to what letter in the keys array
    keybox = [17, 570, 56, 622] # Coordinate for the button on the keyboard. Convert to tuple when used on functions..
    
    keyregion = base.crop(tuple(keybox))
    base.paste(PIL.ImageOps.invert(keyregion), keybox)
    UpdateDisplay()

    # Loop: Get button input
    # WASD arrows, J = Select, K = cancel
    while True:
        inp = GetInput()
        if inp == 'd':
            if letter[1] == 9 or cmp(letter, [3, 8]) == 0:
                continue
            else:
                # Uninvert current selection 
                base.paste(keyregion, keybox)
                # Update variables 
                letter[1] += 1
                keybox[0] += 45
                keybox[2] += 45
                # Invert new selection
                keyregion = base.crop(tuple(keybox))
                base.paste(PIL.ImageOps.invert(keyregion), keybox)
                print keys[letter[0]][letter[1]]
        elif inp == 'a':
            if letter[1] == 0:
                continue
            else:
                # Uninvert current selection 
                base.paste(keyregion, keybox)
                # Update variables 
                letter[1] -= 1
                keybox[0] -= 45
                keybox[2] -= 45
                # Invert new selection
                keyregion = base.crop(tuple(keybox))
                base.paste(PIL.ImageOps.invert(keyregion), keybox)
                print keys[letter[0]][letter[1]]
        elif inp == 'w':
            if letter[0] == 0:
                continue
            else:
                # Uninvert current selection 
                base.paste(keyregion, keybox)
                # Update variables 
                letter[0] -= 1
                keybox[1] -= 56
                keybox[3] -= 56
                # Invert new selection
                keyregion = base.crop(tuple(keybox))
                base.paste(PIL.ImageOps.invert(keyregion), keybox)
                print keys[letter[0]][letter[1]]
        elif inp == 's':
            if letter[0] == 3 or cmp(letter, [2, 9]) == 0:
                continue
            else:
                # Uninvert current selection 
                base.paste(keyregion, keybox)
                # Update variables 
                letter[0] += 1
                keybox[1] += 56
                keybox[3] += 56
                # Invert new selection
                keyregion = base.crop(tuple(keybox))
                base.paste(PIL.ImageOps.invert(keyregion), keybox)
                print keys[letter[0]][letter[1]]    
        elif inp == 'j':
            # Buffer selected key
            pressed = keys[letter[0]][letter[1]]
            print pressed
            if pressed == 127:
                pass
            elif pressed == 0:
                break
            else:
                textbuffer += pressed
                if p_flag:
                    pressed = '*'
                fnt = ImageFont.truetype('resources/fonts/Inconsolata-Bold.ttf', 20)
                draw = ImageDraw.Draw(base)
                draw.text(tuple(crsr), pressed, fill=(0,0,0), font=fnt)
                crsr[0] += 15
        elif inp == 'back':
            # Hide keyboard
            continue
        else:
            continue

        UpdateDisplay()

    keyboard.close


def ShowLogIn():
    global base, textbuffer, crsr, user, p_flag
  
    temp_im = Image.open('resources/ui/screen_login.png')
    base.paste(temp_im, (0,0))
    
    ShowKeyboard()
    username = textbuffer
    print username

    crsr = [83, 415]
    p_flag = True
    ShowKeyboard()
    p_flag = False
    password = textbuffer
    print password

    user = db.LogIn(username, password)
    if user is None:
        draw = ImageDraw.Draw(base)
        textfnt = ImageFont.truetype('resources/fonts/ACaslonPro-Regular.otf', 22)
        draw.text((140, 490), 'Wrong id or password.', fill=(0, 0, 0), font=textfnt)
        UpdateDisplay()
    else:
        ShowLibrary()

    temp_im.close()


def ShowLibrary():
    global base, user, books

    textfnt = ImageFont.truetype('resources/fonts/ACaslonPro-Regular.otf', 25)
    bkfnt = ImageFont.truetype('resources/fonts/ACaslonPro-Regular.otf', 22)
    authfnt = ImageFont.truetype('resources/fonts/ACaslonPro-Regular.otf', 20)
    temp_im = Image.open('resources/ui/screen_library.png').convert('RGB')

    base.paste(temp_im, (0,0))

    draw = ImageDraw.Draw(base)
    name =  user.fname + ' ' + user.mname[0] + '. ' + user.lname
    draw.text((95, 55), name, fill=(0, 0, 0), font=textfnt)

    # List all Books
    books = db.ListBooks(user.uname)
    pages = (len(books) / 8) + 1

    for i in range(0, len(books)):
        draw.text((42, 205 + (i * 58)), books[i].title, fill=(0,0,0,0), font=bkfnt)
        draw.text((42, 230 + (i * 58)) , books[i].author, fill=(0,0,0,0), font=authfnt)

    selected = 0
    box = [32, 198, 448, 254]
    boxregion = base.crop(tuple(box))
    base.paste(PIL.ImageOps.invert(boxregion), box)
    UpdateDisplay()
    while True:
        inp = GetInput()
        if inp == 'w':
            if selected == 0:
                pass
            else:
                base.paste(boxregion, box)
                selected -= 1
                box[1] -= 58
                box[3] -= 58
                boxregion = base.crop(tuple(box))
                base.paste(PIL.ImageOps.invert(boxregion), box)
                UpdateDisplay()
        elif inp == 's':
            print selected
            if selected >= len(books) - 1:
                pass
            else:
                base.paste(boxregion, box)
                selected += 1
                box[1] += 58
                box[3] += 58
                boxregion = base.crop(tuple(box))
                base.paste(PIL.ImageOps.invert(boxregion), box)
                UpdateDisplay()
        elif inp == 'a':
            pass
        elif inp == 'd':
            pass
        elif inp == 'j':
            print books[selected].fpath
            BookView(books[selected])
        elif inp == 'k':
            pass

    temp_im.close()


def BookView(book):
    global base
    temp_im = Image.open('resources/ui/screen_readingview.png').convert('RGB')
    base.paste(temp_im, (0,0))
    titlefnt = ImageFont.truetype('resources/fonts/ACaslonPro-Regular.otf', 22)
    draw = ImageDraw.Draw(base)
    draw.text((42, 38), book.title, fill=(0, 0, 0), font=titlefnt)
    UpdateDisplay()



def Main():
    # Draw the log in screen
    global base, user
    base = Image.open('resources/ui/epd.png').convert('RGB')

    ShowLogIn()
    # UpdateDisplay()
    # ShowKeyboard()

    # Library screen 
    # username = raw_input("ID: ")
    # password = raw_input("Password: ")
    # user = db.LogIn(username, password)

    # if user is not None:
    #     ShowLibrary()
    # else:
    #     print 'Wrong id/pass'


    # UpdateDisplay
    base.close()


if __name__ == '__main__':
    Main()
    # spi.close()
