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


#Parse args
parser = argparse.ArgumentParser()
parser.add_argument("--not-pi",
                    action="store_true",
                    help="Execute the script on a non-Raspberry Pi computer.")
parser.add_argument("--pi", 
                    action="store_true",
                    help="Execute the script on the Raspberry Pi.")
args = parser.parse_args()


keys =  [ #DEL = 127, 0 = OK
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',' J'],
        ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'],
        ['U', 'V', 'W', 'X', 'Y', 'Z', ' ', 127, 0, 0]]
base = None
lastkey = ''


if args.pi:
    import epd


def UpdateDisplay():
    if args.not_pi:
        base.show()
        base.save('cache/screens/screen.png', "PNG")

    if args.pi:
        pass

def GetInput():
    if args.not_pi:
        inp = raw_input("Input: ") #Change this to button input'
        return inp.strip()

    if args.pi:
        return button_press()

def ShowKeyboard():
    global base,lastkey
    keyboard = Image.open('resources/ui/keyboard.png').convert('RGB')
    base.paste(keyboard, (0, 560))

    #Select letter 'A'
    letter = [0, 0] # Corresponds to what letter in the keys array
    keybox = [17, 570, 56, 622] # Coordinate for the button on the keyboard. Convert to tuple when used on functions..
    
    keyregion = base.crop(tuple(keybox))
    base.paste(PIL.ImageOps.invert(keyregion), keybox)
    UpdateDisplay()

    # Loop: Get button input
    while True:
        inp = GetInput()
        if inp == 'done':
            break
        elif inp == 'right':
            if letter[1] == 9 or cmp(letter, [8, 8]) == 0:
                pass
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
                UpdateDisplay()
                print keys[letter[0]][letter[1]]
        elif inp == 'left':
            if letter[1] == 0:
                pass
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
                UpdateDisplay()
                print keys[letter[0]][letter[1]]
            pass
        elif inp == 'up':
            if letter[0] == 0:
                pass
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
                UpdateDisplay()
                print keys[letter[0]][letter[1]]
            pass
        elif inp == 'down':
            if letter[0] == 3 or cmp(letter, [9, 2]) == 0:
                pass
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
                UpdateDisplay()
                print keys[letter[0]][letter[1]]    
            pass
        elif inp == 'select':
            # Buffer selected key
            lastkey = keys[letter[0]][letter[1]]
        elif inp == 'back':
            # Hide keyboard
            pass
        else:
            pass

    keyboard.close


def HideKeyboard():
    pass


def Main():
    # Draw the log in screen
    global base, lastkey
    base = Image.open('resources/ui/epd.png').convert('RGB')
    temp_im = Image.open('resources/ui/screen_login.png')
    base.paste(temp_im, (0,0), temp_im)

    # Code for drawing text on image
    txt = Image.new('RGB', base.size, (255,255,255,0))
    fnt = ImageFont.truetype('resources/fonts/ACaslonPro-Regular.otf', 35)

    ShowKeyboard()

    # Attemp log in
    

    # UpdateDisplay
    base.close()
    temp_im.close()


if __name__ == '__main__':
    Main()
    # spi.close()