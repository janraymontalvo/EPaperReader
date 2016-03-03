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

import PIL.ImageOps
import argparse, db, epub, zipfile, textwrap, html2text
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup


#Parse args
parser = argparse.ArgumentParser()
parser.add_argument("--pi", 
                    action="store_true",
                    help="Execute the script on the Raspberry Pi.")
parser.add_argument("--not-pi",
                    action="store_true",
                    help="Please use this if you don't have a RaspPi")
args = parser.parse_args()
if not (args.pi or args.not_pi):
    parser.print_help()
    parser.error('No parameter given.')

if args.not_pi:
    import os
    pi_dir = '/home/ceruleous/Documents/Documents/GitHub/EPaperReader'

if args.pi:
    import epd
    pi_dir = '/home/pi/EPaperReader'

keys =  [ #DEL = 127, 0 = OK
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
        ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'],
        ['U', 'V', 'W', 'X', 'Y', 'Z', ' ', 127, 0, 0]]
base = None
pressed = ''
keyboardbuffer = ''
crsr = [83, 286] # Cursor for text input from keyboard

def Main():
    # Draw the log in screen
    global base, user
    base = Image.open(pi_dir + '/resources/ui/epd.png').convert('RGB')
    #if args.pi:
     #   epd.update_screen(base)
    #else:
     #   base.show()        
    ShowLogIn()
    base.close()


def PrintText(text, coordinates , fnt):
    ''' Write text to screen '''
    global base
    draw = ImageDraw.Draw(base)
    draw.text(coordinates, text, fill=(0,0,0), font=fnt)


def UpdateDisplay():
    ''' Update the EPD screen '''
    print 'Updating Display'
    now = db.Today()
    temp_im = Image.open(pi_dir + '/resources/ui/element_status_bar.png')
    base.paste(temp_im, (0,0))
    temp_im.close()
    PrintText(now, (260, 2), ImageFont.truetype(pi_dir + '/resources/fonts/OpenSans-Regular.ttf', 18))
    if args.not_pi:
        base.save(pi_dir + 'screen.png', "PNG")
        base.show()
    
    if args.pi:
        epd.update_screen(base)


def GetInput():
    ''' Get input from keyboard or GPIO buttons '''
    if args.not_pi:
        inp = raw_input("Input: ")
        return inp.strip()
    
    if args.pi:
        inp = epd.button_press()
        return inp


def ShowKeyboard(passwordfield=False):
    # TODO: Circular keyboard
    # TODO: Enable numpad
    ''' Keyboard '''
    print 'Showing Keyboard'
    global base, pressed, keyboardbuffer
    keyboardbuffer = ''
    keyboard = Image.open(pi_dir + '/resources/ui/keyboard.png').convert('RGB')
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
                print 'Letter Selected: {0}'.format(keys[letter[0]][letter[1]])
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
                print 'Letter Highlighted: {0}'.format(keys[letter[0]][letter[1]])
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
                print 'Letter Highlighted: {0}'.format(keys[letter[0]][letter[1]])
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
                print 'Letter Highlighted: {0}'.format(keys[letter[0]][letter[1]])   
        elif inp == 'j':
            # Buffer selected key
            pressed = keys[letter[0]][letter[1]]
            print 'Letter Selected: {0}'.format(pressed)
            if pressed == 127:
                # TODO: Erase char
                if keyboardbuffer == '':
                    keyboardbuffer = keyboardbuffer[:-1]
                    crsr[0] -= 15
                    ImageDraw.Draw(base).rectangle(tuple(crsr) + (crsr[0] + 9, crsr[1] + 24), fill=(255,255,255))
                print 'Text Buffer: {0}'.format(keyboardbuffer)
            elif pressed == 0:
                print 'Text Buffer: {0}'.format(keyboardbuffer)
                break
            else:
                keyboardbuffer += pressed
                if passwordfield:
                    pressed = '*'
                
                PrintText(pressed, tuple(crsr), ImageFont.truetype(pi_dir + '/resources/fonts/Inconsolata-Bold.ttf', 20))
                crsr[0] += 15
        elif inp == 'k':
            # Hide keyboard
            continue
        else:
            continue

        UpdateDisplay()

    keyboard.close

# TODO: 
# - Erase character when pressing backspace
def ShowLogIn():
    global base, keyboardbuffer, crsr, user
    print 'Log In View'

    wrong_pass = False

    while True:
        temp_im = Image.open(pi_dir+'/resources/ui/screen_login.png')
        base.paste(temp_im, (0,0))

        # if wrong_pass: 
        #     PrintText('Wrong id or password.', (140, 490), ImageFont.truetype('resources/fonts/ACaslonPro-Regular.otf', 22))
        
        # crsr = [83, 286]
        # ShowKeyboard()   
        # username = keyboardbuffer
        # crsr = [83, 415]
        # ShowKeyboard(True)
        # password = keyboardbuffer

        # user = db.LogIn(username, password)
        user = db.LogIn('201', '123')
        if user is None:
            print "Wrong id or password"
            wrong_pass = True
            continue
        else:
            wrong_pass = False
            ShowLibrary(user)

    # user = db.LogIn('201', '123')
    # ShowLibrary(user)


def ShowLibrary(user):
    global base
    print 'Library View'

    textfnt = ImageFont.truetype(pi_dir + '/resources/fonts/ACaslonPro-Regular.otf', 25)
    bkfnt = ImageFont.truetype(pi_dir + '/resources/fonts/ACaslonPro-Regular.otf', 22)
    authfnt = ImageFont.truetype(pi_dir + '/resources/fonts/ACaslonPro-Regular.otf', 20)
    temp_im = Image.open(pi_dir + '/resources/ui/screen_library.png').convert('RGB')

    while True:
        base.paste(temp_im, (0,0))
        name =  user.fname + ' ' + user.mname[0] + '. ' + user.lname
        PrintText(name, (95, 55), textfnt)
        books = db.ListBooks(user.uname)

        for i in range(0, len(books)):
            PrintText(books[i].title, (42, 205 + (i * 58)), bkfnt)
            PrintText(books[i].author, (42, 230 + (i * 58)), authfnt)

        selected = 0
        box = [32, 198, 448, 254]
        print books[selected].title
        boxregion = base.crop(tuple(box))
        base.paste(PIL.ImageOps.invert(boxregion), box)

        while True:
            UpdateDisplay()
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
                    print "Selected book: {0}".format(books[selected].fpath)       
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
                    print "Selected book: {0}".format(books[selected].fpath)
            elif inp == 'a':
                pass
            elif inp == 'd':
                pass
            elif inp == 'j':
                print books[selected].fpath
                BookView(books[selected])
                break
            elif inp == 'k':
                # Close the view and cleanup
                temp_im.close()
                return



def BookView(book):
    global base
    print 'Book View'

    titlefnt = ImageFont.truetype(pi_dir + '/resources/fonts/ACaslonPro-Regular.otf', 21)
    textfnt = ImageFont.truetype(pi_dir + '/resources/fonts/DejaVuSansMono.ttf', 15)
    temp_im = Image.open(pi_dir + '/resources/ui/screen_readingview.png').convert('RGB')
    pagewrap = textwrap.TextWrapper(width=858, break_long_words=False, replace_whitespace=False)
    linewrap = textwrap.TextWrapper(width=43, break_long_words=True, replace_whitespace=False)
    textregion = (47, 72, 432, 735) # Text box coordinates
    h = html2text.HTML2Text()
    h.ignore_links = True
    
    draw = ImageDraw.Draw(base)
    base.paste(temp_im, (0,0))
    PrintText(book.title, (42, 38), titlefnt)

    # ebook = epub.open_epub(book.fpath)
    ebook = epub.open_epub('test.epub')
    contents = list([i for i in epub.table_of_contents(ebook)])

    cons = 0
    while cons < len(contents):
        print contents[cons]
        soup = BeautifulSoup(ebook.read(contents[cons][1]))
        # chaptertext = epub.textify(unicode(soup.find('body')).encode('utf-8'), maxcol=float("+inf"),)
        chaptertext = h.handle(soup.find('body').prettify())
        paragraphs = chaptertext.splitlines(True)

        lines = []
        for i in paragraphs:
            x = linewrap.wrap(i)

            if x == []:
                lines.append('\n')
            else:
                lines.extend(x)

        line, ctr = 0, 0
        textarea = list(textregion)
        draw.rectangle(textregion, fill=(255,255,255))
        while line < len(lines):
            # width, height = textfnt.getsize(line)
            PrintText(lines[line], (textarea[0], textarea[1]), textfnt)            
            textarea[1] += 16
            line += 1
            ctr += 1

            print 'cons: {0}'.format(cons)
            print 'line: {0}'.format(line)
            # If Text area is full or there is no more text to print...
            if textarea[1] >= 715 or line >= len(lines):
                print line 
                print ctr
                UpdateDisplay()

                inp = GetInput()
                if inp == 'a':
                    textarea = list(textregion)
                    draw.rectangle(textregion, fill=(255,255,255))

                    if line - (ctr * 2) > 0:
                        line -= ctr * 2
                    else:
                        cons -= 2
                        break

                    ctr = 0
                    continue
                elif inp == 'd':
                    textarea = list(textregion)
                    draw.rectangle(textregion, fill=(255,255,255))
                    ctr = 0
                    continue
                elif inp == 'w':
                    continue
                elif inp == 's':
                    continue
                elif inp == 'j':
                    continue
                elif inp == 'k':
                    return

        cons += 1


if __name__ == '__main__':
    Main()
    # spi.close()
