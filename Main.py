import board
import busio
import adafruit_ssd1306
import digitalio
import time
import threading
from gpiozero import Button
from threading import Event
from PIL import Image, ImageDraw, ImageFont
import piir
from piir.io import receive
from piir.decode import decode
from piir.prettify import prettify
import json
import os
import ntpath
import shutil
import pathlib

reset_pin = digitalio.DigitalInOut(board.D4)
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3d, reset=reset_pin)

oled.fill(0)
oled.show()

image = Image.new('1', (oled.width, oled.height))

draw = ImageDraw.Draw(image)

def Clearall():
    draw.rectangle([(0, 0),(128, 64)], fill="#000000")

def show():
    oled.image(image)
    oled.show()

#Start of loading

draw.text((43, 20), "FlipperI", font=ImageFont.load_default(), fill="#ffffff")
    
show()

LoadEvent = Event()

def Loading():
    time.sleep(3)
    while True:
        draw.rectangle([(47, 40), (50, 43)], fill="#ffffff")
        show()
        time.sleep(0.5)
        draw.rectangle([(62, 40), (65, 43)], fill="#ffffff")
        show()
        time.sleep(0.5)
        draw.rectangle([(77, 40), (80, 43)], fill="#ffffff")
        show()
        time.sleep(0.5)
        draw.rectangle([(62, 40), (65, 43)], fill="#000000")
        draw.rectangle([(77, 40), (80, 43)], fill="#000000")
        show()
        if LoadEvent.is_set():
            draw.rectangle([(47, 40), (50, 43)], fill="#000000")
            break



Loadingscreen = threading.Thread(target=Loading)
Loadingscreen.start()
time.sleep(10)
LoadEvent.set()
Loadingscreen.join()
Clearall()

#End of loading

Selected = None

UpButton = Button(17)
DownButton = Button(4)
LeftButton = Button(23)
RightButton = Button(24)
SelectButton = Button(27)

def Main_InfaredBox(show):
    global Selected
    if show == True:
        Selected = "Infared"
        draw.rectangle([(3, 2), (54, 13)], fill="#ffffff")
        draw.rectangle([(4, 3), (53, 12)], fill="#000000")
        draw.text((5, 2), "Infrared", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(3, 2), (54, 13)], fill="#000000")
        draw.rectangle([(4, 3), (53, 12)], fill="#000000")
        draw.text((5, 2), "Infrared", font=ImageFont.load_default(), fill="#ffffff")

def Main_USBBox(show):
    global Selected
    if show == True:
        Selected = "USB"
        draw.rectangle([(3, 14), (47, 24)], fill="#ffffff")
        draw.rectangle([(4, 15), (46, 23)], fill="#000000")
        draw.text((5, 14), "Bad USB", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(3, 14), (47, 24)], fill="#000000")
        draw.rectangle([(4, 15), (46, 23)], fill="#000000")
        draw.text((5, 14), "Bad USB", font=ImageFont.load_default(), fill="#ffffff")
        
def Main_FileBox(show):
    global Selected
    if show == True:
        Selected = "File"
        draw.rectangle([(3, 26), (36, 36)], fill="#ffffff")
        draw.rectangle([(4, 27), (35, 35)], fill="#000000")
        draw.text((5, 26), "Files", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(3, 26), (36, 36)], fill="#000000")
        draw.rectangle([(4, 27), (35, 35)], fill="#000000")
        draw.text((5, 26), "Files", font=ImageFont.load_default(), fill="#ffffff")

def Infared_ReadBox(show):
    global Selected
    if show == True:
        Selected = "IRRead"
        draw.rectangle([(3, 2), (95, 13)], fill="#ffffff")
        draw.rectangle([(4, 3), (94, 12)], fill="#000000")
        draw.text((5, 2), "Read New Device", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(3, 2), (95, 13)], fill="#000000")
        draw.rectangle([(4, 3), (94, 12)], fill="#000000")
        draw.text((5, 2), "Read New Device", font=ImageFont.load_default(), fill="#ffffff")

def Infared_PlayBox(show):
    global Selected
    if show == True:
        Selected = "IRPlay"
        draw.rectangle([(3, 14), (71, 26)], fill="#ffffff")
        draw.rectangle([(4, 15), (70, 25)], fill="#000000")
        draw.text((5, 14), "Play Device", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(3, 14), (71, 26)], fill="#000000")
        draw.rectangle([(4, 15), (70, 25)], fill="#000000")
        draw.text((5, 14), "Play Device", font=ImageFont.load_default(), fill="#ffffff")
        
def Infared_BackBox(show):
    global Selected
    if show == True:
        Selected = "IRBack"
        draw.rectangle([(3, 26), (30, 36)], fill="#ffffff")
        draw.rectangle([(4, 27), (29, 35)], fill="#000000")
        draw.text((5, 26), "Back", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(3, 26), (30, 36)], fill="#000000")
        draw.rectangle([(4, 27), (29, 35)], fill="#000000")
        draw.text((5, 26), "Back", font=ImageFont.load_default(), fill="#ffffff")

def InfaredRead_BackBox(show):
    global Selected
    if show == True:
        Selected = "IRBack"
        draw.rectangle([(3, 26), (30, 36)], fill="#ffffff")
        draw.rectangle([(4, 27), (29, 35)], fill="#000000")
        draw.text((5, 26), "Back", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(3, 26), (30, 36)], fill="#000000")
        draw.rectangle([(4, 27), (29, 35)], fill="#000000")
        draw.text((5, 26), "Back", font=ImageFont.load_default(), fill="#ffffff")
        
def InfaredRead_CancelBox(show):
    global Selected
    if show == True:
        Selected = "IRRCancel"
        draw.rectangle([(3, 50), (42, 60)], fill="#ffffff")
        draw.rectangle([(4, 51), (41, 59)], fill="#000000")
        draw.text((5, 50), "Cancel", font=ImageFont.load_default(), fill="#ffffff")

def InfaredRead_SaveBox(show):
    global Selected
    if show == True:
        Selected = "IRRSave"
        draw.rectangle([(121, 51), (95, 60)], fill="#ffffff")
        draw.rectangle([(120, 52), (96, 59)], fill="#000000")
        draw.text((97, 50), "Save", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(121, 51), (95, 60)], fill="#000000")
        draw.rectangle([(120, 52), (96, 59)], fill="#000000")
        draw.text((97, 50), "Save", font=ImageFont.load_default(), fill="#ffffff")
        
def InfaredRead_ReReadBox(show):
    global Selected
    if show == True:
        Selected = "IRRReRead"
        draw.rectangle([(3, 50), (42, 60)], fill="#ffffff")
        draw.rectangle([(4, 51), (41, 59)], fill="#000000")
        draw.text((5, 50), "ReRead", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(3, 50), (42, 60)], fill="#000000")
        draw.rectangle([(4, 51), (41, 59)], fill="#000000")
        draw.text((5, 50), "ReRead", font=ImageFont.load_default(), fill="#ffffff")
        
KeyBoardObject = None  

def InfaredRead_NameBox(show):
    global Selected
    global KeyBoardObject
    if show == True:
        Selected = "IRRName"
        draw.rectangle([(3, 3), (112, 15)], fill="#ffffff")
        draw.rectangle([(4, 4), (111, 14)], fill="#000000")
        draw.text((5, 2), "Name:", font=ImageFont.load_default(), fill="#ffffff")
        draw.text((33, 3), "_____________", font=ImageFont.load_default(), fill="#ffffff")
        draw.text((35, 2), KeyBoardObject, font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(3, 3), (112, 15)], fill="#000000")
        draw.rectangle([(4, 4), (111, 14)], fill="#000000")
        draw.text((5, 2), "Name:", font=ImageFont.load_default(), fill="#ffffff")
        draw.text((33, 3), "_____________", font=ImageFont.load_default(), fill="#ffffff")
        draw.text((35, 2), KeyBoardObject, font=ImageFont.load_default(), fill="#ffffff")

def Keyboard_QBox(show):
    global Selected
    if show == True:
        Selected = "KQ"
        draw.rectangle([(1, 31), (9, 39)], fill="#ffffff") #q box
        draw.text((2, 28), "q", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(1, 31), (9, 39)], fill="#000000") #q box
        draw.text((2, 28), "q", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_WBox(show):
    global Selected
    if show == True:
        Selected = "KW"
        draw.rectangle([(10, 31), (17, 39)], fill="#ffffff") #w box
        draw.text((11, 28), "w", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(10, 31), (17, 39)], fill="#000000") #w box
        draw.text((11, 28), "w", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_EBox(show):
    global Selected
    if show == True:
        Selected = "KE"
        draw.rectangle([(19, 31), (25, 38)], fill="#ffffff") #e box
        draw.text((20, 28), "e", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(19, 31), (25, 38)], fill="#000000") #e box
        draw.text((20, 28), "e", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_RBox(show):
    global Selected
    if show == True:
        Selected = "KR"
        draw.rectangle([(28, 31), (35, 38)], fill="#ffffff") #r box
        draw.text((29, 28), "r", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(28, 31), (35, 38)], fill="#000000") #r box
        draw.text((29, 28), "r", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_TBox(show):
    global Selected
    if show == True:
        Selected = "KT"
        draw.rectangle([(37, 29), (44, 38)], fill="#ffffff") #t box
        draw.text((38, 28), "t", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(37, 29), (44, 38)], fill="#000000") #t box
        draw.text((38, 28), "t", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_YBox(show):
    global Selected
    if show == True:
        Selected = "KY"
        draw.rectangle([(46, 31), (53, 39)], fill="#ffffff") #y box
        draw.text((47, 28), "y", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(46, 31), (53, 39)], fill="#000000") #y box
        draw.text((47, 28), "y", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_UBox(show):
    global Selected
    if show == True:
        Selected = "KU"
        draw.rectangle([(55, 31), (62, 37)], fill="#ffffff") #u box
        draw.text((56, 28), "u", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(55, 31), (62, 37)], fill="#000000") #u box
        draw.text((56, 28), "u", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_IBox(show):
    global Selected
    if show == True:
        Selected = "KI"
        draw.rectangle([(64, 29), (71, 38)], fill="#ffffff") #i box
        draw.text((65, 28), "i", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(64, 29), (71, 38)], fill="#000000") #i box
        draw.text((65, 28), "i", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_OBox(show):
    global Selected
    if show == True:
        Selected = "KO"
        draw.rectangle([(73, 31), (80, 38)], fill="#ffffff") #o box
        draw.text((74, 28), "o", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(73, 31), (80, 38)], fill="#000000") #o box
        draw.text((74, 28), "o", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_PBox(show):
    global Selected
    if show == True:
        Selected = "KP"
        draw.rectangle([(82, 31), (88, 38)], fill="#ffffff") #p box
        draw.text((83, 28), "p", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(82, 31), (88, 38)], fill="#000000") #p box
        draw.text((83, 28), "p", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_0Box(show):
    global Selected
    if show == True:
        Selected = "K0"
        draw.rectangle([(91, 29), (97, 38)], fill="#ffffff") #0 box
        draw.text((92, 28), "0", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(91, 29), (97, 38)], fill="#000000") #0 box
        draw.text((92, 28), "0", font=ImageFont.load_default(), fill="#ffffff")
    
def Keyboard_1Box(show):
    global Selected
    if show == True:
        Selected = "K1"
        draw.rectangle([(100, 29), (107, 38)], fill="#ffffff") #1 box
        draw.text((101, 28), "1", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(100, 29), (107, 38)], fill="#000000") #1 box
        draw.text((101, 28), "1", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_2Box(show):
    global Selected
    if show == True:
        Selected = "K2"
        draw.rectangle([(109, 29), (115, 38)], fill="#ffffff") #2 box
        draw.text((110, 28), "2", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(109, 29), (115, 38)], fill="#000000") #2 box
        draw.text((110, 28), "2", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_3Box(show):
    global Selected
    if show == True:
        Selected = "K3"
        draw.rectangle([(118, 29), (124, 38)], fill="#ffffff") #3 box
        draw.text((119, 28), "3", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(118, 29), (124, 38)], fill="#000000") #3 box
        draw.text((119, 28), "3", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_ABox(show):
    global Selected
    if show == True:
        Selected = "KA"
        draw.rectangle([(1, 41), (8, 49)], fill="#ffffff") #a box
        draw.text((2, 38), "a", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(1, 41), (8, 49)], fill="#000000") #a box
        draw.text((2, 38), "a", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_SBox(show):
    global Selected
    if show == True:
        Selected = "KS"
        draw.rectangle([(10, 41), (17, 49)], fill="#ffffff") #s box
        draw.text((11, 38), "s", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(10, 41), (17, 49)], fill="#000000") #s box
        draw.text((11, 38), "s", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_DBox(show):
    global Selected
    if show == True:
        Selected = "KD"
        draw.rectangle([(19, 40), (26, 49)], fill="#ffffff") #d box
        draw.text((20, 39), "d", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(19, 40), (26, 49)], fill="#000000") #d box
        draw.text((20, 39), "d", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_FBox(show):
    global Selected
    if show == True:
        Selected = "KF"
        draw.rectangle([(28, 40), (35, 49)], fill="#ffffff")
        draw.text((29, 39), "f", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(28, 40), (35, 49)], fill="#000000")
        draw.text((29, 39), "f", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_GBox(show):
    global Selected
    if show == True:
        Selected = "KG"
        draw.rectangle([(37, 40), (44, 48)], fill="#ffffff") #g box
        draw.text((38, 37), "g", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(37, 40), (44, 48)], fill="#000000") #g box
        draw.text((38, 37), "g", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_HBox(show):
    global Selected
    if show == True:
        Selected = "KH"
        draw.rectangle([(46, 41), (53, 49)], fill="#ffffff") #h box
        draw.text((47, 40), "h", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(46, 41), (53, 49)], fill="#000000") #h box
        draw.text((47, 40), "h", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_JBox(show):
    global Selected
    if show == True:
        Selected = "KJ"
        draw.rectangle([(55, 39), (62, 49)], fill="#ffffff") #j box
        draw.text((56, 38), "j", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(55, 39), (62, 49)], fill="#000000") #j box
        draw.text((56, 38), "j", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_KBox(show):
    global Selected
    if show == True:
        Selected = "KK"
        draw.rectangle([(64, 40), (71, 49)], fill="#ffffff") #k box
        draw.text((65, 39), "k", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(64, 40), (71, 49)], fill="#000000") #k box
        draw.text((65, 39), "k", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_LBox(show):
    global Selected
    if show == True:
        Selected = "KL"
        draw.rectangle([(73, 39), (80, 47)], fill="#ffffff") #l box
        draw.text((74, 38), "l", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(73, 39), (80, 47)], fill="#000000") #l box
        draw.text((74, 38), "l", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_DelBox(show):
    global Selected
    if show == True:
        Selected = "KDel"
        draw.rectangle([(82, 41), (98, 45)], fill="#ffffff")
        draw.text((82, 38), "<--", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(82, 41), (98, 45)], fill="#000000")
        draw.text((82, 38), "<--", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_4Box(show):
    global Selected
    if show == True:
        Selected = "K4"
        draw.rectangle([(100, 39), (107, 47)], fill="#ffffff") #4 box
        draw.text((101, 38), "4", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(100, 39), (107, 47)], fill="#000000") #4 box
        draw.text((101, 38), "4", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_5Box(show):
    global Selected
    if show == True:
        Selected = "K5"
        draw.rectangle([(109, 39), (115, 47)], fill="#ffffff") #5 box
        draw.text((110, 38), "5", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(109, 39), (115, 47)], fill="#000000") #5 box
        draw.text((110, 38), "5", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_6Box(show):
    global Selected
    if show == True:
        Selected = "K6"
        draw.rectangle([(118, 39), (124, 47)], fill="#ffffff") #6 box
        draw.text((119, 38), "6", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(118, 39), (124, 47)], fill="#000000") #6 box
        draw.text((119, 38), "6", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_ZBox(show):
    global Selected
    if show == True:
        Selected = "KZ"
        draw.rectangle([(1, 51), (8, 59)], fill="#ffffff") #z box
        draw.text((2, 48), "z", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(1, 51), (8, 59)], fill="#000000") #z box
        draw.text((2, 48), "z", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_XBox(show):
    global Selected
    if show == True:
        Selected = "KX"
        draw.rectangle([(10, 51), (17, 59)], fill="#ffffff") #x box
        draw.text((11, 48), "x", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(10, 51), (17, 59)], fill="#000000") #x box
        draw.text((11, 48), "x", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_CBox(show):
    global Selected
    if show == True:
        Selected = "KC"
        draw.rectangle([(19, 51), (26, 59)], fill="#ffffff") #c box
        draw.text((20, 48), "c", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(19, 51), (26, 59)], fill="#000000") #c box
        draw.text((20, 48), "c", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_VBox(show):
    global Selected
    if show == True:
        Selected = "KV"
        draw.rectangle([(28, 51), (35, 59)], fill="#ffffff") #v box
        draw.text((29, 48), "v", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(28, 51), (35, 59)], fill="#000000") #v box
        draw.text((29, 48), "v", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_BBox(show):
    global Selected
    if show == True:
        Selected = "KB"
        draw.rectangle([(37, 51), (44, 59)], fill="#ffffff") #b box
        draw.text((38, 50), "b", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(37, 51), (44, 59)], fill="#000000") #b box
        draw.text((38, 50), "b", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_NBox(show):
    global Selected
    if show == True:
        Selected = "KN"
        draw.rectangle([(46, 51), (53, 59)], fill="#ffffff") #n box
        draw.text((47, 48), "n", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(46, 51), (53, 59)], fill="#000000") #n box
        draw.text((47, 48), "n", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_MBox(show):
    global Selected
    if show == True:
        Selected = "KM"
        draw.rectangle([(55, 51), (62, 59)], fill="#ffffff") #m box
        draw.text((56, 48), "m", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(55, 51), (62, 59)], fill="#000000") #m box
        draw.text((56, 48), "m", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard__Box(show):
    global Selected
    if show == True:
        Selected = "K_"
        draw.rectangle([(64, 51), (71, 59)], fill="#ffffff") #_ box
        draw.text((65, 48), "_", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(64, 51), (71, 59)], fill="#000000") #_ box
        draw.text((65, 48), "_", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_SaveBox(show):
    global Selected
    if show == True:
        Selected = "KSave"
        draw.rectangle([(74, 50), (98, 57)], fill="#ffffff")
        draw.text((75, 48), "Save", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(74, 50), (98, 57)], fill="#000000")
        draw.text((75, 48), "Save", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_7Box(show):
    global Selected
    if show == True:
        Selected = "K7"
        draw.rectangle([(100, 49), (107, 59)], fill="#ffffff") #7 box
        draw.text((101, 48), "7", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(100, 49), (107, 59)], fill="#000000") #7 box
        draw.text((101, 48), "7", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_8Box(show):
    global Selected
    if show == True:
        Selected = "K8"
        draw.rectangle([(109, 49), (115, 59)], fill="#ffffff") #8 box
        draw.text((110, 48), "8", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(109, 49), (115, 59)], fill="#000000") #8 box
        draw.text((110, 48), "8", font=ImageFont.load_default(), fill="#ffffff")
        
def Keyboard_9Box(show):
    global Selected
    if show == True:
        Selected = "K9"
        draw.rectangle([(118, 49), (124, 59)], fill="#ffffff") #9 box
        draw.text((119, 48), "9", font=ImageFont.load_default(), fill="#000000")
    else:
        draw.rectangle([(118, 49), (124, 59)], fill="#000000") #9 box
        draw.text((119, 48), "9", font=ImageFont.load_default(), fill="#ffffff")

# Keyboard start

def ShowKeyboard():
    #Boxes
    draw.rectangle([(81, 40), (99, 46)], fill="#ffffff")
    draw.rectangle([(82, 41), (98, 45)], fill="#000000")
    
    draw.rectangle([(73, 49), (99, 58)], fill="#ffffff")
    draw.rectangle([(74, 50), (98, 57)], fill="#000000")
    
    
    #first row
    draw.text((2, 28), "q", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((11, 28), "w", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((20, 28), "e", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((29, 28), "r", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((38, 28), "t", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((47, 28), "y", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((56, 28), "u", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((65, 28), "i", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((74, 28), "o", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((83, 28), "p", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((92, 28), "0", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((101, 28), "1", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((110, 28), "2", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((119, 28), "3", font=ImageFont.load_default(), fill="#ffffff")
    
    #second row
    draw.text((2, 38), "a", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((11, 38), "s", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((20, 39), "d", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((29, 39), "f", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((38, 37), "g", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((47, 40), "h", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((56, 38), "j", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((65, 39), "k", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((74, 38), "l", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((82, 38), "<--", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((101, 38), "4", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((110, 38), "5", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((119, 38), "6", font=ImageFont.load_default(), fill="#ffffff")
    
    #third row
    draw.text((2, 48), "z", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((11, 48), "x", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((20, 48), "c", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((29, 48), "v", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((38, 50), "b", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((47, 48), "n", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((56, 48), "m", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((65, 48), "_", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((75, 48), "Save", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((101, 48), "7", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((110, 48), "8", font=ImageFont.load_default(), fill="#ffffff")
    draw.text((119, 48), "9", font=ImageFont.load_default(), fill="#ffffff")


draw.text((72, 52), "Main Menu", font=ImageFont.load_default(), fill="#ffffff")
draw.text((5, 2), "Infrared", font=ImageFont.load_default(), fill="#ffffff")
draw.text((5, 14), "Bad USB", font=ImageFont.load_default(), fill="#ffffff")
draw.text((5, 26), "Files", font=ImageFont.load_default(), fill="#ffffff")
Main_InfaredBox(True)

Active = False

CurrentKeyboardFocus = None

def start():
    global CurrentKeyboardFocus
    global Active
    global KeyBoardObject
    print("reading")
    keys = {}

    while True:
        data = decode(receive(22))
        if data:
            break
    if Active:
        Active = False
        keys["Data"] = data
        KeyBoardObject = "IRDevice"
        CurrentKeyboardFocus = "IRRead"
        bufferfile=open("BUFFERFILE.json", "w")
        bufferfile.write(json.dumps(prettify(keys), indent=2))
        bufferfile.close()
        Clearall()
        draw.text((2, 20), "Successfully read", font=ImageFont.load_default(), fill="#ffffff")
        draw.text((2, 29), "your IR Device!", font=ImageFont.load_default(), fill="#ffffff")
        draw.text((5, 2), "Name:", font=ImageFont.load_default(), fill="#ffffff")
        draw.text((97, 50), "Save", font=ImageFont.load_default(), fill="#ffffff")
        draw.text((5, 50), "ReRead", font=ImageFont.load_default(), fill="#ffffff")
        draw.text((33, 3), "_____________", font=ImageFont.load_default(), fill="#ffffff")
        draw.text((35, 2), (KeyBoardObject), font=ImageFont.load_default(), fill="#ffffff")
        InfaredRead_SaveBox(True)
        show()

def ClearKeyboardText():
    draw.rectangle([(33, 2), (130, 15)], fill="#000000")
    
def AddKeyboardText(letter):
    global KeyBoardObject
    draw.text((35, 2), (KeyBoardObject + letter), font=ImageFont.load_default(), fill="#ffffff")
    KeyBoardObject = KeyBoardObject + letter
    
def RemoveKeyboardText():
    global KeyBoardObject
    draw.text((35, 2), KeyBoardObject[:-1], font=ImageFont.load_default(), fill="#ffffff")
    KeyBoardObject = KeyBoardObject[:-1]

def Infared_PPlayBox(show):
    global Selected
    if show == True:
        Selected = "IRPPlay"
        draw.rectangle([(8, 20), (64, 32)], fill="#ffffff")
        draw.rectangle([(9, 21), (63, 31)], fill="#000000")
        draw.text((10, 20), "Play File", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(8, 20), (64, 32)], fill="#000000")
        draw.rectangle([(9, 21), (63, 31)], fill="#000000")
        draw.text((10, 20), "Play File", font=ImageFont.load_default(), fill="#ffffff")
        
def USB_PlayBox(show):
    global Selected
    if show == True:
        Selected = "USBPlay"
        draw.rectangle([(8, 20), (82, 32)], fill="#ffffff")
        draw.rectangle([(9, 21), (81, 31)], fill="#000000")
        draw.text((10, 20), "Execute File", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(8, 20), (82, 32)], fill="#000000")
        draw.rectangle([(9, 21), (81, 31)], fill="#000000")
        draw.text((10, 20), "Execute File", font=ImageFont.load_default(), fill="#ffffff")
        
def File_BackBox(show):
    global Selected
    if show == True:
        Selected = "USBMenuBack"
        draw.rectangle([(8, 35), (35, 45)], fill="#ffffff")
        draw.rectangle([(9, 36), (34, 44)], fill="#000000")
        draw.text((10, 35), "Back", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(8, 35), (35, 45)], fill="#000000")
        draw.rectangle([(9, 36), (34, 44)], fill="#000000")
        draw.text((10, 35), "Back", font=ImageFont.load_default(), fill="#ffffff")

def Infared_MenuBackBox(show):
    global Selected
    if show == True:
        Selected = "IRMenuBack"
        draw.rectangle([(2, 49), (16, 57)], fill="#ffffff")
        draw.rectangle([(3, 50), (15, 56)], fill="#000000")
        draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(2, 49), (16, 57)], fill="#000000")
        draw.rectangle([(3, 50), (15, 56)], fill="#000000")
        draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
        
def IRFilesFunc(show):
    global Selected
    if show == True:
        Selected = "IRFilesFunc"
        draw.text((22, 4), ">", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.text((22, 4), ">", font=ImageFont.load_default(), fill="#000000")

def USBFiles(show):
    global Selected
    if show == True:
        Selected = "USBFiles"
        draw.text((22, 19), ">", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.text((22, 19), ">", font=ImageFont.load_default(), fill="#000000")

def DriveFiles(show):
    global Selected
    if show == True:
        Selected = "DriveFiles"
        draw.text((22, 34), ">", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.text((22, 34), ">", font=ImageFont.load_default(), fill="#000000")

F1, F2, F3, F4 = None, None, None, None

def FileSelection1(show):
    global Selected
    global F1, F2, F3, F4
    if not F1 == "None":
        if show == True:
            Selected = "F1"
            draw.text((22, 4), ">", font=ImageFont.load_default(), fill="#ffffff")
        else:
            draw.text((22, 4), ">", font=ImageFont.load_default(), fill="#000000")
        
def FileSelection2(show):
    global Selected
    global F1, F2, F3, F4
    if not F2 == "None":
        if show == True:
            Selected = "F2"
            draw.text((22, 19), ">", font=ImageFont.load_default(), fill="#ffffff")
        else:
            draw.text((22, 19), ">", font=ImageFont.load_default(), fill="#000000")

FileSelected = None

def FileSelection3(show):
    global Selected
    global F1, F2, F3, F4
    global FileSelected
    if not F3 == "None":
        if show == True:
            Selected = "F3"
            draw.text((22, 34), ">", font=ImageFont.load_default(), fill="#ffffff")
        else:
            draw.text((22, 34), ">", font=ImageFont.load_default(), fill="#000000")
        
def FileSelection4(show):
    global Selected
    global F1, F2, F3, F4
    if not F4 == "None":
        if show == True:
            Selected = "F4"
            draw.text((22, 49), ">", font=ImageFont.load_default(), fill="#ffffff")
        else:
            draw.text((22, 49), ">", font=ImageFont.load_default(), fill="#000000")
            
def MoveFile(show):
    global Selected
    if show == True:
        Selected = "MoveFile"
        draw.rectangle([(8, 16), (64, 26)], fill="#ffffff")
        draw.rectangle([(9, 17), (63, 25)], fill="#000000")
        draw.text((10, 16), "Move File", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(8, 16), (64, 26)], fill="#000000")
        draw.rectangle([(9, 17), (63, 25)], fill="#000000")
        draw.text((10, 16), "Move File", font=ImageFont.load_default(), fill="#ffffff")
        
        
def DeleteFile(show):
    global Selected
    if show == True:
        Selected = "DeleteFile"
        draw.rectangle([(8, 27), (76, 37)], fill="#ffffff")
        draw.rectangle([(9, 28), (75, 36)], fill="#000000")
        draw.text((10, 27), "Delete File", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(8, 27), (76, 37)], fill="#000000")
        draw.rectangle([(9, 28), (75, 36)], fill="#000000")
        draw.text((10, 27), "Delete File", font=ImageFont.load_default(), fill="#ffffff")
        
def RenameFile(show):
    global Selected
    if show == True:
        Selected = "RenameFile"
        draw.rectangle([(8, 38), (76, 48)], fill="#ffffff")
        draw.rectangle([(9, 39), (75, 47)], fill="#000000")
        draw.text((10, 38), "ReName File", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(8, 38), (76, 48)], fill="#000000")
        draw.rectangle([(9, 39), (75, 47)], fill="#000000")
        draw.text((10, 38), "ReName File", font=ImageFont.load_default(), fill="#ffffff")

def FileSelectionBack(show):
    global Selected
    if show == True:
        Selected = "FileSelectionBack"
        draw.rectangle([(8, 49), (35, 59)], fill="#ffffff")
        draw.rectangle([(9, 50), (34, 58)], fill="#000000")
        draw.text((10, 49), "Back", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(8, 49), (35, 59)], fill="#000000")
        draw.rectangle([(9, 50), (34, 58)], fill="#000000")
        draw.text((10, 49), "Back", font=ImageFont.load_default(), fill="#ffffff")

def MoveFileIR(show):
    global Selected
    if show == True:
        Selected = "MoveFileIR"
        draw.rectangle([(8, 16), (23, 26)], fill="#ffffff")
        draw.rectangle([(9, 17), (22, 25)], fill="#000000")
        draw.text((10, 16), "IR", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(8, 16), (23, 26)], fill="#000000")
        draw.rectangle([(9, 17), (22, 25)], fill="#000000")
        draw.text((10, 16), "IR", font=ImageFont.load_default(), fill="#ffffff")
        
def MoveFileUSB(show):
    global Selected
    if show == True:
        Selected = "MoveFileUSB"
        draw.rectangle([(8, 16), (52, 28)], fill="#ffffff")
        draw.rectangle([(9, 17), (51, 27)], fill="#000000")
        draw.text((10, 16), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(8, 16), (52, 28)], fill="#000000")
        draw.rectangle([(9, 17), (51, 27)], fill="#000000")
        draw.text((10, 16), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")

def MoveFileDrives(show):
    global Selected
    if show == True:
        Selected = "MoveFileDrives"
        draw.rectangle([(8, 27), (47, 37)], fill="#ffffff")
        draw.rectangle([(9, 28), (46, 36)], fill="#000000")
        draw.text((10, 27), "Drives", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(8, 27), (47, 37)], fill="#000000")
        draw.rectangle([(9, 28), (46, 36)], fill="#000000")
        draw.text((10, 27), "Drives", font=ImageFont.load_default(), fill="#ffffff")
        
def MoveFileCancel(show):
    global Selected
    if show == True:
        Selected = "MoveFileCancel"
        draw.rectangle([(8, 38), (47, 48)], fill="#ffffff")
        draw.rectangle([(9, 39), (46, 47)], fill="#000000")
        draw.text((10, 38), "Cancel", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(8, 38), (47, 48)], fill="#000000")
        draw.rectangle([(9, 39), (46, 47)], fill="#000000")
        draw.text((10, 38), "Cancel", font=ImageFont.load_default(), fill="#ffffff")

def DeleteFileYes(show):
    global Selected
    if show == True:
        Selected = "DeleteFileYes"
        draw.rectangle([(8, 17), (29, 26)], fill="#ffffff")
        draw.rectangle([(9, 18), (28, 25)], fill="#000000")
        draw.text((10, 16), "Yes", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(8, 17), (29, 26)], fill="#000000")
        draw.rectangle([(9, 18), (28, 25)], fill="#000000")
        draw.text((10, 16), "Yes", font=ImageFont.load_default(), fill="#ffffff")
        
def DeleteFileNo(show):
    global Selected
    if show == True:
        Selected = "DeleteFileNo"
        draw.rectangle([(8, 28), (22, 37)], fill="#ffffff")
        draw.rectangle([(9, 29), (21, 36)], fill="#000000")
        draw.text((10, 27), "No", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(8, 28), (22, 37)], fill="#000000")
        draw.rectangle([(9, 29), (21, 36)], fill="#000000")
        draw.text((10, 27), "No", font=ImageFont.load_default(), fill="#ffffff")
        
def FlashOk(show):
    global Selected
    if show == True:
        Selected = "FlashOk"
        draw.rectangle([(8, 27), (23, 37)], fill="#ffffff")
        draw.rectangle([(9, 28), (22, 36)], fill="#000000")
        draw.text((10, 27), "Ok", font=ImageFont.load_default(), fill="#ffffff")
    else:
        draw.rectangle([(8, 27), (23, 37)], fill="#000000")
        draw.rectangle([(9, 26), (22, 36)], fill="#000000")
        draw.text((10, 27), "Ok", font=ImageFont.load_default(), fill="#ffffff")

def GetChildren(Drive):
    rootdir = Drive
    Files = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        Files.append(d)
    return Files

All_Pages = 0
Current_Page = 1
File_Manager = None
FileSorter = None
Flash_Drive = None

def CheckFlash():
    global Flash_Drive
    rootdir = r"/media/astroberry"
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            Flash_Drive = d

def ButtonEvents():
    while True:
        global Selected
        global Active
        global KeyBoardObject
        global All_Pages
        global Current_Page
        global F1, F2, F3, F4
        global File_Manager
        global FileSorter
        global Flash_Drive
        
        def DisplayPage(number, flist):
            ReturningList = []
            for x in flist:
                if x[1] == number:
                    ReturningList.append(x)
            try:
                a = ReturningList[0]
            except Exception:
                a = "None"
                
            try:
                b = ReturningList[1]
            except Exception:
                b = "None"
                
            try:
                c = ReturningList[2]
            except Exception:
                c = "None"
                
            try:
                d = ReturningList[3]
            except Exception:
                d = "None"

            return a, b, c, d
                    
        
        def File_Selection(files):
            global F1, F2, F3, F4
            global All_Pages
            global Current_Page
            global File_Manager
            All_Pages = (len(files)//4) + (len(files)%4)
            Files = files
            File_Manager = []
            Page = 1
            Counter = 1
            
            for x in files:
                if Counter > 4:
                    Page = Page + 1
                    Counter = 1
                File_Manager.append([x, Page, Counter])
                Counter = Counter + 1
               
            
            F1, F2, F3, F4 = DisplayPage(1, File_Manager)
            if not F1 == "None":
                draw.text((30, 3), ntpath.basename(F1[0]), font=ImageFont.load_default(), fill="#ffffff")
            
            if not F2 == "None":
                draw.text((30, 18), ntpath.basename(F2[0]), font=ImageFont.load_default(), fill="#ffffff")
                
            if not F3 == "None":
                draw.text((30, 33), ntpath.basename(F3[0]), font=ImageFont.load_default(), fill="#ffffff")
                
            if not F4 == "None":
                draw.text((30, 48), ntpath.basename(F4[0]), font=ImageFont.load_default(), fill="#ffffff")
            
            if F1 == "None":
                Infared_MenuBackBox(True)
            else:
                FileSelection1(True)
            show()
                    
        if UpButton.is_pressed:
            if Selected == "USBMenuBack":
                File_BackBox(False)
                USB_PlayBox(True)
                show()
            elif Selected == "IRPBack":
                File_BackBox(False)
                if FileSorter == "IRPlay":
                    Infared_PPlayBox(True)
                elif FileSorter == "USB":
                    USB_PlayBox(True)
                show()
            elif Selected == "F1":
                if not Current_Page == 1:
                    Current_Page = Current_Page - 1
                    F1, F2, F3, F4 = DisplayPage(Current_Page, File_Manager)
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    
                    if not F1 == "None":
                        draw.text((30, 3), ntpath.basename(F1[0]), font=ImageFont.load_default(), fill="#ffffff")
            
                    if not F2 == "None":
                        draw.text((30, 18), ntpath.basename(F2[0]), font=ImageFont.load_default(), fill="#ffffff")
                        
                    if not F3 == "None":
                        draw.text((30, 33), ntpath.basename(F3[0]), font=ImageFont.load_default(), fill="#ffffff")
                        
                    if not F4 == "None":
                        draw.text((30, 48), ntpath.basename(F4[0]), font=ImageFont.load_default(), fill="#ffffff")
                    FileSelection4(True)
                    show()
            if Selected == "F2":
                FileSelection2(False)
                FileSelection3(False)
                FileSelection4(False)
                FileSelection1(True)
                show()
            elif Selected == "F3":
                FileSelection3(False)
                FileSelection1(False)
                FileSelection4(False)
                FileSelection2(True)
                show()
            elif Selected == "F4":
                FileSelection4(False)
                FileSelection2(False)
                FileSelection1(False)
                FileSelection3(True)
                show()
            elif Selected == "USB":
                Main_USBBox(False)
                Main_InfaredBox(True)
                show()
            elif Selected == "File":
                Main_FileBox(False)
                Main_USBBox(True)
                show()
            elif Selected == "IRPlay":
                Infared_PlayBox(False)
                Infared_ReadBox(True)
                show()
            elif Selected == "IRBack":
                Infared_BackBox(False)
                Infared_PlayBox(True)
                show()
            elif Selected == "IRRSave":
                InfaredRead_SaveBox(False)
                InfaredRead_NameBox(True)
                show()
            elif Selected == "IRRReRead":
                InfaredRead_ReReadBox(False)
                InfaredRead_NameBox(True)
                show()
            elif Selected == "KZ":
                Keyboard_ZBox(False)
                Keyboard_ABox(True)
                show()
            elif Selected == "KA":
                Keyboard_ABox(False)
                Keyboard_QBox(True)
                show()
            elif Selected == "KX":
                Keyboard_XBox(False)
                Keyboard_SBox(True)
                show()
            elif Selected == "KS":
                Keyboard_SBox(False)
                Keyboard_WBox(True)
                show()
            elif Selected == "KC":
                Keyboard_CBox(False)
                Keyboard_DBox(True)
                show()
            elif Selected == "KD":
                Keyboard_DBox(False)
                Keyboard_EBox(True)
                show()
            elif Selected == "KV":
                Keyboard_VBox(False)
                Keyboard_FBox(True)
                show()
            elif Selected == "KF":
                Keyboard_FBox(False)
                Keyboard_RBox(True)
                show()
            elif Selected == "KB":
                Keyboard_BBox(False)
                Keyboard_GBox(True)
                show()
            elif Selected == "KG":
                Keyboard_GBox(False)
                Keyboard_TBox(True)
                show()
            elif Selected == "KN":
                Keyboard_NBox(False)
                Keyboard_HBox(True)
                show()
            elif Selected == "KH":
                Keyboard_HBox(False)
                Keyboard_YBox(True)
                show()
            elif Selected == "KM":
                Keyboard_MBox(False)
                Keyboard_JBox(True)
                show()
            elif Selected == "KJ":
                Keyboard_JBox(False)
                Keyboard_UBox(True)
                show()
            elif Selected == "K_":
                Keyboard__Box(False)
                Keyboard_KBox(True)
                show()
            elif Selected == "KK":
                Keyboard_KBox(False)
                Keyboard_IBox(True)
                show()
            elif Selected == "KK":
                Keyboard_KBox(False)
                Keyboard_IBox(True)
                show()
            elif Selected == "KL":
                Keyboard_LBox(False)
                Keyboard_OBox(True)
                show()
            elif Selected == "KSave":
                Keyboard_SaveBox(False)
                Keyboard_DelBox(True)
                show()
            elif Selected == "KDel":
                Keyboard_DelBox(False)
                Keyboard_0Box(True)
                show()
            elif Selected == "K7":
                Keyboard_7Box(False)
                Keyboard_4Box(True)
                show()
            elif Selected == "K4":
                Keyboard_4Box(False)
                Keyboard_1Box(True)
                show()
            elif Selected == "K8":
                Keyboard_8Box(False)
                Keyboard_5Box(True)
                show()
            elif Selected == "K5":
                Keyboard_5Box(False)
                Keyboard_2Box(True)
                show()
            elif Selected == "K9":
                Keyboard_9Box(False)
                Keyboard_6Box(True)
                show()
            elif Selected == "K6":
                Keyboard_6Box(False)
                Keyboard_3Box(True)
                show()
            elif Selected == "USBFiles":
                USBFiles(False)
                IRFilesFunc(True)
                show()
            elif Selected == "DriveFiles":
                DriveFiles(False)
                USBFiles(True)
                show()
            elif Selected == "FileSelectionBack":
                FileSelectionBack(False)
                RenameFile(True)
                show()
            elif Selected == "RenameFile":
                RenameFile(False)
                DeleteFile(True)
                show()
            elif Selected == "DeleteFile":
                DeleteFile(False)
                MoveFile(True)
                show()
            elif Selected == "MoveFileDrives":
                MoveFileDrives(False)
                if FileSorter == "IRFile":
                    MoveFileIR(True)
                elif FileSorter == "USBFile":
                    MoveFileUSB(True)
                show()
            elif Selected == "MoveFileCancel":
                MoveFileCancel(False)
                MoveFileDrives(True)
                show()
            elif Selected == "DeleteFileNo":
                DeleteFileNo(False)
                DeleteFileYes(True)
                show()
            time.sleep(0.1)
        
        if DownButton.is_pressed:
            if Selected == "IRFilesFunc":
                IRFilesFunc(False)
                USBFiles(True)
                show()
            elif Selected == "DeleteFileYes":
                DeleteFileYes(False)
                DeleteFileNo(True)
                show()
            elif Selected == "MoveFileDrives":
                MoveFileDrives(False)
                MoveFileCancel(True)
                show()
            elif Selected == "MoveFileUSB":
                MoveFileUSB(False)
                MoveFileDrives(True)
                show()
            elif Selected == "MoveFileIR":
                MoveFileIR(False)
                MoveFileDrives(True)
                show()
            elif Selected == "MoveFile":
                MoveFile(False)
                DeleteFile(True)
                show()
            elif Selected == "DeleteFile":
                DeleteFile(False)
                RenameFile(True)
                show()
            elif Selected == "RenameFile":
                RenameFile(False)
                FileSelectionBack(True)
                show()
            elif Selected == "USBFiles":
                USBFiles(False)
                DriveFiles(True)
                show()
            elif Selected == "USBPlay":
                USB_PlayBox(False)
                File_BackBox(True)
                show()
            elif Selected == "IRPPlay":
                if FileSorter == "IRPlay":
                    Infared_PPlayBox(False)
                elif FileSorter == "USB":
                    USB_PlayBox(False)
                File_BackBox(True)
                show()
            elif Selected == "F1":
                if F2 == "None":
                    pass
                else:
                    FileSelection1(False)
                    FileSelection2(True)
                show()
            elif Selected == "F2":
                if F3 == "None":
                    pass
                else:
                    FileSelection2(False)
                    FileSelection3(True)
                show()
            elif Selected == "F3":
                if F4 == "None":
                    pass
                else:
                    FileSelection3(False)
                    FileSelection4(True)
                show()
            elif Selected == "F4":
                if not All_Pages == 1:
                    F1, F2, F3, F4 = DisplayPage(Current_Page + 1, File_Manager)
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    Current_Page = Current_Page + 1
                    if not F1 == "None":
                        draw.text((30, 3), ntpath.basename(F1[0]), font=ImageFont.load_default(), fill="#ffffff")
            
                    if not F2 == "None":
                        draw.text((30, 18), ntpath.basename(F2[0]), font=ImageFont.load_default(), fill="#ffffff")
                        
                    if not F3 == "None":
                        draw.text((30, 33), ntpath.basename(F3[0]), font=ImageFont.load_default(), fill="#ffffff")
                        
                    if not F4 == "None":
                        draw.text((30, 48), ntpath.basename(F4[0]), font=ImageFont.load_default(), fill="#ffffff")
                    FileSelection1(True)
                    show()
            elif Selected == "Infared":
                Main_InfaredBox(False)
                Main_USBBox(True)
                show()
            elif Selected == "USB":
                Main_USBBox(False)
                Main_FileBox(True)
                show()
            elif Selected == "IRRead":
                Infared_ReadBox(False)
                Infared_PlayBox(True)
                show()
            elif Selected == "IRPlay":
                Infared_PlayBox(False)
                Infared_BackBox(True)
                show()
            elif Selected == "IRRName":
                InfaredRead_NameBox(False)
                InfaredRead_SaveBox(True)
                show()
            elif Selected == "KQ":
                Keyboard_QBox(False)
                Keyboard_ABox(True)
                show()
            elif Selected == "KA":
                Keyboard_ABox(False)
                Keyboard_ZBox(True)
                show()
            elif Selected == "KW":
                Keyboard_WBox(False)
                Keyboard_SBox(True)
                show()
            elif Selected == "KS":
                Keyboard_SBox(False)
                Keyboard_XBox(True)
                show()
            elif Selected == "KE":
                Keyboard_EBox(False)
                Keyboard_DBox(True)
                show()
            elif Selected == "KD":
                Keyboard_DBox(False)
                Keyboard_CBox(True)
                show()
            elif Selected == "KR":
                Keyboard_RBox(False)
                Keyboard_FBox(True)
                show()
            elif Selected == "KF":
                Keyboard_FBox(False)
                Keyboard_VBox(True)
                show()
            elif Selected == "KF":
                Keyboard_FBox(False)
                Keyboard_VBox(True)
                show()
            elif Selected == "KT":
                Keyboard_TBox(False)
                Keyboard_GBox(True)
                show()
            elif Selected == "KG":
                Keyboard_GBox(False)
                Keyboard_BBox(True)
                show()
            elif Selected == "KY":
                Keyboard_YBox(False)
                Keyboard_HBox(True)
                show()
            elif Selected == "KH":
                Keyboard_HBox(False)
                Keyboard_NBox(True)
                show()
            elif Selected == "KU":
                Keyboard_UBox(False)
                Keyboard_JBox(True)
                show()
            elif Selected == "KJ":
                Keyboard_JBox(False)
                Keyboard_MBox(True)
                show()
            elif Selected == "KI":
                Keyboard_IBox(False)
                Keyboard_KBox(True)
                show()
            elif Selected == "KK":
                Keyboard_KBox(False)
                Keyboard__Box(True)
                show()
            elif Selected == "KO":
                Keyboard_OBox(False)
                Keyboard_LBox(True)
                show()
            elif Selected == "KL":
                Keyboard_LBox(False)
                Keyboard_SaveBox(True)
                show()
            elif Selected == "KP":
                Keyboard_PBox(False)
                Keyboard_DelBox(True)
                show()
            elif Selected == "KDel":
                Keyboard_DelBox(False)
                Keyboard_SaveBox(True)
                show()
            elif Selected == "K0":
                Keyboard_0Box(False)
                Keyboard_DelBox(True)
                show()
            elif Selected == "K1":
                Keyboard_1Box(False)
                Keyboard_4Box(True)
                show()
            elif Selected == "K4":
                Keyboard_4Box(False)
                Keyboard_7Box(True)
                show()
            elif Selected == "K2":
                Keyboard_2Box(False)
                Keyboard_5Box(True)
                show()
            elif Selected == "K5":
                Keyboard_5Box(False)
                Keyboard_8Box(True)
                show()
            elif Selected == "K3":
                Keyboard_3Box(False)
                Keyboard_6Box(True)
                show()
            elif Selected == "K6":
                Keyboard_6Box(False)
                Keyboard_9Box(True)
                show()
            time.sleep(0.1)
            
        if LeftButton.is_pressed:
            if Selected == "IRFilesFunc":
                IRFilesFunc(False)
                Infared_MenuBackBox(True)
                show()
            elif Selected == "USBFiles":
                USBFiles(False)
                Infared_MenuBackBox(True)
                show()
            elif Selected == "DriveFiles":
                DriveFiles(False)
                Infared_MenuBackBox(True)
                show()
            elif Selected == "IRRSave":
                InfaredRead_SaveBox(False)
                InfaredRead_ReReadBox(True)
                show()
            elif Selected == "K3":
                Keyboard_3Box(False)
                Keyboard_2Box(True)
                show()
            elif Selected == "K2":
                Keyboard_2Box(False)
                Keyboard_1Box(True)
                show()
            elif Selected == "K1":
                Keyboard_1Box(False)
                Keyboard_0Box(True)
                show()
            elif Selected == "K0":
                Keyboard_0Box(False)
                Keyboard_PBox(True)
                show()
            elif Selected == "KP":
                Keyboard_PBox(False)
                Keyboard_OBox(True)
                show()
            elif Selected == "KO":
                Keyboard_OBox(False)
                Keyboard_IBox(True)
                show()
            elif Selected == "KI":
                Keyboard_IBox(False)
                Keyboard_UBox(True)
                show()
            elif Selected == "KU":
                Keyboard_UBox(False)
                Keyboard_YBox(True)
                show()
            elif Selected == "KY":
                Keyboard_YBox(False)
                Keyboard_TBox(True)
                show()
            elif Selected == "KT":
                Keyboard_TBox(False)
                Keyboard_RBox(True)
                show()
            elif Selected == "KR":
                Keyboard_RBox(False)
                Keyboard_EBox(True)
                show()
            elif Selected == "KE":
                Keyboard_EBox(False)
                Keyboard_WBox(True)
                show()
            elif Selected == "KW":
                Keyboard_WBox(False)
                Keyboard_QBox(True)
                show()
            elif Selected == "K6":
                Keyboard_6Box(False)
                Keyboard_5Box(True)
                show()
            elif Selected == "K5":
                Keyboard_5Box(False)
                Keyboard_4Box(True)
                show()
            elif Selected == "K4":
                Keyboard_4Box(False)
                Keyboard_DelBox(True)
                show()
            elif Selected == "KDel":
                Keyboard_DelBox(False)
                Keyboard_LBox(True)
                show()
            elif Selected == "KL":
                Keyboard_LBox(False)
                Keyboard_KBox(True)
                show()
            elif Selected == "KK":
                Keyboard_KBox(False)
                Keyboard_JBox(True)
                show()
            elif Selected == "KJ":
                Keyboard_JBox(False)
                Keyboard_HBox(True)
                show()
            elif Selected == "KH":
                Keyboard_HBox(False)
                Keyboard_GBox(True)
                show()
            elif Selected == "KG":
                Keyboard_GBox(False)
                Keyboard_FBox(True)
                show()
            elif Selected == "KF":
                Keyboard_FBox(False)
                Keyboard_DBox(True)
                show()
            elif Selected == "KD":
                Keyboard_DBox(False)
                Keyboard_SBox(True)
                show()
            elif Selected == "KS":
                Keyboard_SBox(False)
                Keyboard_ABox(True)
                show()
            elif Selected == "K9":
                Keyboard_9Box(False)
                Keyboard_8Box(True)
                show()
            elif Selected == "K8":
                Keyboard_8Box(False)
                Keyboard_7Box(True)
                show()
            elif Selected == "K7":
                Keyboard_7Box(False)
                Keyboard_SaveBox(True)
                show()
            elif Selected == "KSave":
                Keyboard_SaveBox(False)
                Keyboard__Box(True)
                show()
            elif Selected == "K_":
                Keyboard__Box(False)
                Keyboard_MBox(True)
                show()
            elif Selected == "KM":
                Keyboard_MBox(False)
                Keyboard_NBox(True)
                show()
            elif Selected == "KN":
                Keyboard_NBox(False)
                Keyboard_BBox(True)
                show()
            elif Selected == "KB":
                Keyboard_BBox(False)
                Keyboard_VBox(True)
                show()
            elif Selected == "KV":
                Keyboard_VBox(False)
                Keyboard_CBox(True)
                show()
            elif Selected == "KC":
                Keyboard_CBox(False)
                Keyboard_XBox(True)
                show()
            elif Selected == "KX":
                Keyboard_XBox(False)
                Keyboard_ZBox(True)
                show()
            elif Selected == "F1":
                FileSelection1(False)
                Infared_MenuBackBox(True)
                print(Selected)
                show()
            elif Selected == "F2":
                FileSelection2(False)
                Infared_MenuBackBox(True)
                show()
            elif Selected == "F3":
                FileSelection3(False)
                Infared_MenuBackBox(True)
                show()
            elif Selected == "F4":
                FileSelection4(False)
                Infared_MenuBackBox(True)
                show()
            time.sleep(0.1)
            
        if RightButton.is_pressed:
            if Selected == "IRMenuBack":
                if F1 == None:
                    pass
                else:
                    Infared_MenuBackBox(False)
                    FileSelection1(True)
                    
                if FileSorter == "File":
                    Infared_MenuBackBox(False)
                    IRFilesFunc(True)
                    print("e")
                    show()
                        
                print(FileSorter)
                show()
            elif Selected == "IRRReRead":
                InfaredRead_ReReadBox(False)
                InfaredRead_SaveBox(True)
                show()
            elif Selected == "KQ":
                Keyboard_QBox(False)
                Keyboard_WBox(True)
                show()
            elif Selected == "KW":
                Keyboard_WBox(False)
                Keyboard_EBox(True)
                show()
            elif Selected == "KE":
                Keyboard_EBox(False)
                Keyboard_RBox(True)
                show()
            elif Selected == "KR":
                Keyboard_RBox(False)
                Keyboard_TBox(True)
                show()
            elif Selected == "KT":
                Keyboard_TBox(False)
                Keyboard_YBox(True)
                show()
            elif Selected == "KY":
                Keyboard_YBox(False)
                Keyboard_UBox(True)
                show()
            elif Selected == "KU":
                Keyboard_UBox(False)
                Keyboard_IBox(True)
                show()
            elif Selected == "KI":
                Keyboard_IBox(False)
                Keyboard_OBox(True)
                show()
            elif Selected == "KO":
                Keyboard_OBox(False)
                Keyboard_PBox(True)
                show()
            elif Selected == "KP":
                Keyboard_PBox(False)
                Keyboard_0Box(True)
                show()
            elif Selected == "K0":
                Keyboard_0Box(False)
                Keyboard_1Box(True)
                show()
            elif Selected == "K1":
                Keyboard_1Box(False)
                Keyboard_2Box(True)
                show()
            elif Selected == "K2":
                Keyboard_2Box(False)
                Keyboard_3Box(True)
                show()
            elif Selected == "KA":
                Keyboard_ABox(False)
                Keyboard_SBox(True)
                show()
            elif Selected == "KS":
                Keyboard_SBox(False)
                Keyboard_DBox(True)
                show()
            elif Selected == "KD":
                Keyboard_DBox(False)
                Keyboard_FBox(True)
                show()
            elif Selected == "KF":
                Keyboard_FBox(False)
                Keyboard_GBox(True)
                show()
            elif Selected == "KG":
                Keyboard_GBox(False)
                Keyboard_HBox(True)
                show()
            elif Selected == "KH":
                Keyboard_HBox(False)
                Keyboard_JBox(True)
                show()
            elif Selected == "KJ":
                Keyboard_JBox(False)
                Keyboard_KBox(True)
                show()
            elif Selected == "KK":
                Keyboard_KBox(False)
                Keyboard_LBox(True)
                show()
            elif Selected == "KL":
                Keyboard_LBox(False)
                Keyboard_DelBox(True)
                show()
            elif Selected == "KDel":
                Keyboard_DelBox(False)
                Keyboard_4Box(True)
                show()
            elif Selected == "K4":
                Keyboard_4Box(False)
                Keyboard_5Box(True)
                show()
            elif Selected == "K5":
                Keyboard_5Box(False)
                Keyboard_6Box(True)
                show()
            elif Selected == "KZ":
                Keyboard_ZBox(False)
                Keyboard_XBox(True)
                show()
            elif Selected == "KX":
                Keyboard_XBox(False)
                Keyboard_CBox(True)
                show()
            elif Selected == "KC":
                Keyboard_CBox(False)
                Keyboard_VBox(True)
                show()
            elif Selected == "KV":
                Keyboard_VBox(False)
                Keyboard_BBox(True)
                show()
            elif Selected == "KB":
                Keyboard_BBox(False)
                Keyboard_NBox(True)
                show()
            elif Selected == "KN":
                Keyboard_NBox(False)
                Keyboard_MBox(True)
                show()
            elif Selected == "KM":
                Keyboard_MBox(False)
                Keyboard__Box(True)
                show()
            elif Selected == "K_":
                Keyboard__Box(False)
                Keyboard_SaveBox(True)
                show()
            elif Selected == "KSave":
                Keyboard_SaveBox(False)
                Keyboard_7Box(True)
                show()
            elif Selected == "K7":
                Keyboard_7Box(False)
                Keyboard_8Box(True)
                show()
            elif Selected == "K8":
                Keyboard_8Box(False)
                Keyboard_9Box(True)
                show()
            time.sleep(0.1)

        if SelectButton.is_pressed:
            if Selected == "Infared":
                Clearall()
                draw.text((5, 2), "Read New Device", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((5, 14), "Play Device", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((5, 26), "Back", font=ImageFont.load_default(), fill="#ffffff")
                Infared_ReadBox(True)
                show()
            elif Selected == "IRRead":
                Active=True
                Clearall()
                draw.text((25, 2), "Reading Device", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((7, 20), "Scan your IR Device", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((53, 29), "Now!", font=ImageFont.load_default(), fill="#ffffff")
                InfaredRead_CancelBox(True)
                show()
                threading.Thread(target=start).start()
            elif Selected == "IRRCancel":
                Active=False
                Clearall()
                draw.text((5, 2), "Read New Device", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((5, 14), "Play Device", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((5, 26), "Back", font=ImageFont.load_default(), fill="#ffffff")
                Infared_ReadBox(True)
                show()
            elif Selected == "IRRReRead":
                os.remove(r"BUFFERFILE.json")
                Active=True
                Clearall()
                draw.text((25, 2), "Reading Device", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((7, 20), "Scan your IR Device", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((53, 29), "Now!", font=ImageFont.load_default(), fill="#ffffff")
                InfaredRead_CancelBox(True)
                show()
                threading.Thread(target=start).start()
            elif Selected == "IRRName":
                InfaredRead_NameBox(False)
                Selected = None
                Clearall()
                ShowKeyboard()
                draw.text((5, 2), "Name:", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((35, 2), KeyBoardObject, font=ImageFont.load_default(), fill="#ffffff")
                Keyboard_QBox(True)
                show()
            elif Selected == "IRRSave":
                Files = GetChildren("/home/astroberry/Desktop/FlipperI/Files/IR/")
                Files2 = []
                for x in Files:
                    Files2.append(ntpath.basename(x))
                
                Can_Do = True
                count = 0
                for x in Files2:
                    if Files2[count].split(".")[0] == KeyBoardObject:
                        Can_Do = False
                        break
                    count = count + 1
                
                if Can_Do == True:
                    os.rename("BUFFERFILE.json", ("/home/astroberry/Desktop/FlipperI/Files/IR/" + KeyBoardObject + ".json"))
                    Clearall()
                    draw.text((5, 2), "Read New Device", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 14), "Play Device", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 26), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    Infared_ReadBox(True)
                    show()
                else:
                    draw.text((2, 40), "File Exists with name", font=ImageFont.load_default(), fill="#ffffff")
                    show()
                    time.sleep(1.5)
                    draw.text((2, 40), "File Exists with name", font=ImageFont.load_default(), fill="#000000")
                    show()
                    
            elif Selected == "IRBack":
                Clearall()
                draw.text((72, 52), "Main Menu", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((5, 2), "Infrared", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((5, 14), "Bad USB", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((5, 26), "Files", font=ImageFont.load_default(), fill="#ffffff")
                Main_InfaredBox(True)
                show()
            elif Selected == "IRPlay":
                FileSorter = "IRPlay"
                Clearall()
                draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                IRFiles = GetChildren(r"/home/astroberry/Desktop/FlipperI/Files/IR")
                File_Selection(IRFiles)
                show()
            elif Selected == "KQ":
                ClearKeyboardText()
                AddKeyboardText("q")
                show()
            elif Selected == "KW":
                ClearKeyboardText()
                AddKeyboardText("w")
                show()
            elif Selected == "KE":
                ClearKeyboardText()
                AddKeyboardText("e")
                show()
            elif Selected == "KR":
                ClearKeyboardText()
                AddKeyboardText("r")
                show()
            elif Selected == "KT":
                ClearKeyboardText()
                AddKeyboardText("t")
                show()
            elif Selected == "KY":
                ClearKeyboardText()
                AddKeyboardText("y")
                show()
            elif Selected == "KU":
                ClearKeyboardText()
                AddKeyboardText("u")
                show()
            elif Selected == "KI":
                ClearKeyboardText()
                AddKeyboardText("i")
                show()
            elif Selected == "KO":
                ClearKeyboardText()
                AddKeyboardText("o")
                show()
            elif Selected == "KP":
                ClearKeyboardText()
                AddKeyboardText("p")
                show()
            elif Selected == "K0":
                ClearKeyboardText()
                AddKeyboardText("0")
                show()
            elif Selected == "K1":
                ClearKeyboardText()
                AddKeyboardText("1")
                show()
            elif Selected == "K2":
                ClearKeyboardText()
                AddKeyboardText("2")
                show()
            elif Selected == "K3":
                ClearKeyboardText()
                AddKeyboardText("3")
                show()
            elif Selected == "KA":
                ClearKeyboardText()
                AddKeyboardText("a")
                show()
            elif Selected == "KS":
                ClearKeyboardText()
                AddKeyboardText("s")
                show()
            elif Selected == "KD":
                ClearKeyboardText()
                AddKeyboardText("d")
                show()
            elif Selected == "KF":
                ClearKeyboardText()
                AddKeyboardText("f")
                show()
            elif Selected == "KG":
                ClearKeyboardText()
                AddKeyboardText("g")
                show()
            elif Selected == "KH":
                ClearKeyboardText()
                AddKeyboardText("h")
                show()
            elif Selected == "KJ":
                ClearKeyboardText()
                AddKeyboardText("j")
                show()
            elif Selected == "KK":
                ClearKeyboardText()
                AddKeyboardText("k")
                show()
            elif Selected == "KL":
                ClearKeyboardText()
                AddKeyboardText("l")
                show()
            elif Selected == "KDel":
                ClearKeyboardText()
                RemoveKeyboardText()
                show()
            elif Selected == "K4":
                ClearKeyboardText()
                AddKeyboardText("4")
                show()
            elif Selected == "K5":
                ClearKeyboardText()
                AddKeyboardText("5")
                show()
            elif Selected == "K6":
                ClearKeyboardText()
                AddKeyboardText("6")
                show()
            elif Selected == "KZ":
                ClearKeyboardText()
                AddKeyboardText("z")
                show()
            elif Selected == "KX":
                ClearKeyboardText()
                AddKeyboardText("x")
                show()
            elif Selected == "KC":
                ClearKeyboardText()
                AddKeyboardText("c")
                show()
            elif Selected == "KV":
                ClearKeyboardText()
                AddKeyboardText("v")
                show()
            elif Selected == "KB":
                ClearKeyboardText()
                AddKeyboardText("b")
                show()
            elif Selected == "KN":
                ClearKeyboardText()
                AddKeyboardText("n")
                show()
            elif Selected == "KM":
                ClearKeyboardText()
                AddKeyboardText("m")
                show()
            elif Selected == "K_":
                ClearKeyboardText()
                AddKeyboardText(" ")
                show()
            elif Selected == "KSave":
                global CurrentKeyboardFocus
                if CurrentKeyboardFocus == "IRRead":
                    Clearall()
                    draw.text((2, 20), "Successfully read", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((2, 29), "your IR Device!", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 2), "Name:", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((97, 50), "Save", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 50), "ReRead", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((33, 3), "_____________", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((35, 2), (KeyBoardObject), font=ImageFont.load_default(), fill="#ffffff")
                    InfaredRead_SaveBox(True)
                elif CurrentKeyboardFocus == "FileRename":
                    suffix = ntpath.basename(FileSelected[0]).split(".")[1]
                    
                    if FileSorter == "IRFile":
                        os.rename(FileSelected[0], "/home/astroberry/Desktop/FlipperI/Files/IR/" + KeyBoardObject+ ".json")
                    elif FileSorter == "USBFile":
                        os.rename(FileSelected[0], "/home/astroberry/Desktop/FlipperI/Files/Bad_USB/" + KeyBoardObject+ ".py")
                    elif FileSorter == "DriveFile":
                        if suffix == "json":
                            os.rename(FileSelected[0], Flash_Drive + "/" + KeyBoardObject+ ".json")
                        elif suffix == "py":
                            os.rename(FileSelected[0], Flash_Drive + "/" + KeyBoardObject+ ".py")
                    FileSorter = "File"
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                    IRFilesFunc(True)
                    show()
            elif Selected == "K7":
                ClearKeyboardText()
                AddKeyboardText("7")
                show()
            elif Selected == "K8":
                ClearKeyboardText()
                AddKeyboardText("8")
                show()
            elif Selected == "K9":
                ClearKeyboardText()
                AddKeyboardText("9")
                show()
            elif Selected == "F1":
                if FileSorter == "IRPlay":
                    Clearall()
                    FileSelected = F1
                    draw.text((10, 3), ntpath.basename(F1[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 20), "Play File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 35), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    Infared_PPlayBox(True)
                    show()
                elif FileSorter == "USB":
                    Clearall()
                    FileSelected = F1
                    draw.text((10, 3), ntpath.basename(F1[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 20), "Execute File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 35), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    USB_PlayBox(True)
                    show()
                elif FileSorter == "IRFile":
                    Clearall()
                    FileSelected = F1
                    draw.text((10, 3), ntpath.basename(F1[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 16), "Move File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Delete File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 38), "ReName File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 49), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    MoveFile(True)
                    show()
                elif FileSorter == "USBFile":
                    Clearall()
                    FileSelected = F1
                    draw.text((10, 3), ntpath.basename(F1[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 16), "Move File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Delete File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 38), "ReName File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 49), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    MoveFile(True)
                    show()
                elif FileSorter == "DriveFile":
                    Clearall()
                    FileSelected = F1
                    draw.text((10, 3), ntpath.basename(F1[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 16), "Move File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Delete File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 38), "ReName File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 49), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    MoveFile(True)
                    show()
            elif Selected == "F2":
                if FileSorter == "IRPlay":
                    Clearall()
                    FileSelected = F2
                    draw.text((10, 3), ntpath.basename(F2[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 20), "Play File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 35), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    Infared_PPlayBox(True)
                    show()
                elif FileSorter == "USB":
                    Clearall()
                    FileSelected = F2
                    draw.text((10, 3), ntpath.basename(F2[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 20), "Execute File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 35), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    USB_PlayBox(True)
                    show()
                elif FileSorter == "IRFile":
                    Clearall()
                    FileSelected = F2
                    draw.text((10, 3), ntpath.basename(F2[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 16), "Move File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Delete File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 38), "ReName File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 49), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    MoveFile(True)
                    show()
                elif FileSorter == "USBFile":
                    Clearall()
                    FileSelected = F2
                    draw.text((10, 3), ntpath.basename(F2[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 16), "Move File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Delete File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 38), "ReName File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 49), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    MoveFile(True)
                    show()
                elif FileSorter == "DriveFile":
                    Clearall()
                    FileSelected = F2
                    draw.text((10, 3), ntpath.basename(F2[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 16), "Move File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Delete File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 38), "ReName File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 49), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    MoveFile(True)
                    show()
            elif Selected == "F3":
                if FileSorter == "IRPlay":
                    Clearall()
                    FileSelected = F3
                    draw.text((10, 3), ntpath.basename(F3[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 20), "Play File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 35), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    Infared_PPlayBox(True)
                    show()
                elif FileSorter == "USB":
                    Clearall()
                    FileSelected = F3
                    draw.text((10, 3), ntpath.basename(F3[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 20), "Execute File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 35), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    USB_PlayBox(True)
                    show()
                elif FileSorter == "IRFile":
                    Clearall()
                    FileSelected = F3
                    draw.text((10, 3), ntpath.basename(F3[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 16), "Move File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Delete File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 38), "ReName File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 49), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    MoveFile(True)
                    show()
                elif FileSorter == "USBFile":
                    Clearall()
                    FileSelected = F3
                    draw.text((10, 3), ntpath.basename(F3[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 16), "Move File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Delete File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 38), "ReName File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 49), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    MoveFile(True)
                    show()
                elif FileSorter == "DriveFile":
                    Clearall()
                    FileSelected = F3
                    draw.text((10, 3), ntpath.basename(F3[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 16), "Move File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Delete File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 38), "ReName File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 49), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    MoveFile(True)
                    show()
            elif Selected == "F4":
                if FileSorter == "IRPlay":
                    Clearall()
                    FileSelected = F4
                    draw.text((10, 3), ntpath.basename(F4[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 20), "Play File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 35), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    Infared_PPlayBox(True)
                    show()
                elif FileSorter == "USB":
                    Clearall()
                    FileSelected = F4
                    draw.text((10, 3), ntpath.basename(F4[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 20), "Execute File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 35), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    USB_PlayBox(True)
                    show()
                elif FileSorter == "IRFile":
                    Clearall()
                    FileSelected = F4
                    draw.text((10, 3), ntpath.basename(F4[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 16), "Move File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Delete File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 38), "ReName File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 49), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    MoveFile(True)
                    show()
                elif FileSorter == "USBFile":
                    Clearall()
                    FileSelected = F4
                    draw.text((10, 3), ntpath.basename(F4[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 16), "Move File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Delete File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 38), "ReName File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 49), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    MoveFile(True)
                    show()
                elif FileSorter == "DriveFile":
                    Clearall()
                    FileSelected = F4
                    draw.text((10, 3), ntpath.basename(F4[0]), font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 16), "Move File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Delete File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 38), "ReName File", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 49), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    MoveFile(True)
                    show()
            elif Selected == "USBPlay":
                 os.system("python3 " + FileSelected[0])
                 draw.text((10, 50), "File Executed", font=ImageFont.load_default(), fill="#ffffff")
                 show()
                 time.sleep(1.5)
                 draw.text((10, 50), "File Executed", font=ImageFont.load_default(), fill="#000000")
                 show()
            elif Selected == "USBMenuBack":
                if FileSorter == "IRPlay":
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    IRFiles = GetChildren(r"/home/astroberry/Desktop/FlipperI/Files/IR")
                    File_Selection(IRFiles)
                    show()
                elif FileSorter == "USB":
                    FileSorter = "USB"
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    Files = GetChildren(r"/home/astroberry/Desktop/FlipperI/Files/Bad_USB")
                    File_Selection(Files)
                    print(Selected)
                    show()
                elif FileSorter == "File":
                    Clearall()
                    draw.text((72, 52), "Main Menu", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 2), "Infrared", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 14), "Bad USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 26), "Files", font=ImageFont.load_default(), fill="#ffffff")
                    Main_InfaredBox(True)
                    show()
                elif FileSorter == "IRFile":
                    FileSorter = "File"
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                    IRFilesFunc(True)
                    show()
                elif FileSorter == "USBFile":
                    FileSorter = "File"
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                    IRFilesFunc(True)
                    show()
                elif FileSorter == "DriveFile":
                    FileSorter = "File"
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                    IRFilesFunc(True)
                    show()
            elif Selected == "IRPPlay":
                piir.Remote(FileSelected[0], 25).send("Data")
                time.sleep(0.3)
            elif Selected == "IRPBack":
                Clearall()
                draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                IRFiles = GetChildren(r"/home/astroberry/Desktop/FlipperI/Files/IR")
                File_Selection(IRFiles)
                show()
            elif Selected == "IRMenuBack":
                if FileSorter == "IRPlay":
                    Infared_MenuBackBox(False)
                    Clearall()
                    draw.text((5, 2), "Read New Device", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 14), "Play Device", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 26), "Back", font=ImageFont.load_default(), fill="#ffffff")
                    Infared_ReadBox(True)
                    FileSorter = None
                    show()
                elif FileSorter == "USB":
                    Clearall()
                    draw.text((72, 52), "Main Menu", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 2), "Infrared", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 14), "Bad USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 26), "Files", font=ImageFont.load_default(), fill="#ffffff")
                    Main_InfaredBox(True)
                    show()
                elif FileSorter == "File":
                    Clearall()
                    draw.text((72, 52), "Main Menu", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 2), "Infrared", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 14), "Bad USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((5, 26), "Files", font=ImageFont.load_default(), fill="#ffffff")
                    Main_InfaredBox(True)
                    show()
                elif FileSorter == "IRFile":
                    FileSorter = "File"
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                    IRFilesFunc(True)
                elif FileSorter == "USBFile":
                    FileSorter = "File"
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                    IRFilesFunc(True)
                    show()
                elif FileSorter == "DriveFile":
                    FileSorter = "File"
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                    IRFilesFunc(True)
                    show()
                show()
            elif Selected == "USB":
                FileSorter = "USB"
                Clearall()
                draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                Files = GetChildren(r"/home/astroberry/Desktop/FlipperI/Files/Bad_USB")
                File_Selection(Files)
                show()
            elif Selected == "File":
                FileSorter = "File"
                Clearall()
                draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                IRFilesFunc(True)
                show()
            elif Selected == "IRFilesFunc":
                FileSorter = "IRFile"
                Clearall()
                draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                Files = GetChildren(r"/home/astroberry/Desktop/FlipperI/Files/IR")
                File_Selection(Files)
                show()
            elif Selected == "USBFiles":
                FileSorter = "USBFile"
                Clearall()
                draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                Files = GetChildren(r"/home/astroberry/Desktop/FlipperI/Files/Bad_USB")
                File_Selection(Files)
                show()
            elif Selected == "DriveFiles":
                CheckFlash()
                if not Flash_Drive == None:
                    FileSorter = "DriveFile"
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    Files = GetChildren(Flash_Drive)
                    Files2 = GetChildren(Flash_Drive)
                    for x in Files:
                        if not pathlib.Path(ntpath.basename(x)).suffix == ".json":
                            Files.remove(x)
                            
                    for x in Files2:
                        if not pathlib.Path(ntpath.basename(x)).suffix == ".py":
                            Files2.remove(x)
                    
                    File_Selection(Files + Files2)
                    show()
                else:
                    Clearall()
                    draw.text((10, 3), "No Drives Inserted", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Ok", font=ImageFont.load_default(), fill="#ffffff")
                    FlashOk(True)
                    show()
            elif Selected == "MoveFile":
                if FileSorter == "IRFile":
                    Clearall()
                    draw.text((10, 3), "Move File:", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 16), "IR", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 38), "Cancel", font=ImageFont.load_default(), fill="#ffffff")
                    MoveFileIR(True)
                    show()
                elif FileSorter == "USBFile":
                    Clearall()
                    draw.text((10, 3), "Move File:", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 16), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 27), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((10, 38), "Cancel", font=ImageFont.load_default(), fill="#ffffff")
                    MoveFileUSB(True)
                    show()
                elif FileSorter == "DriveFile":
                    suffix = ntpath.basename(FileSelected[0]).split(".")[1]
                    if suffix == "json":
                        Clearall()
                        draw.text((10, 3), "Move File:", font=ImageFont.load_default(), fill="#ffffff")
                        draw.text((10, 16), "IR", font=ImageFont.load_default(), fill="#ffffff")
                        draw.text((10, 27), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                        draw.text((10, 38), "Cancel", font=ImageFont.load_default(), fill="#ffffff")
                        MoveFileIR(True)
                        show()
                    elif suffix == "py":
                        Clearall()
                        draw.text((10, 3), "Move File:", font=ImageFont.load_default(), fill="#ffffff")
                        draw.text((10, 16), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                        draw.text((10, 27), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                        draw.text((10, 38), "Cancel", font=ImageFont.load_default(), fill="#ffffff")
                        MoveFileUSB(True)
                        show()
            elif Selected == "MoveFileIR":
                if FileSorter == "DriveFile":
                    shutil.move(FileSelected[0], ("/home/astroberry/Desktop/FlipperI/Files/IR/"))
                    FileSorter = "File"
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                    IRFilesFunc(True)
                    show()
                else:
                    FileSorter = "File"
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                    IRFilesFunc(True)
                    show()
            elif Selected == "MoveFileUSB":
                if FileSorter == "DriveFile":
                    shutil.move(FileSelected[0], ("/home/astroberry/Desktop/FlipperI/Files/Bad_USB/"))
                    FileSorter = "File"
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                    IRFilesFunc(True)
                    show()
                else:
                    FileSorter = "File"
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                    IRFilesFunc(True)
                    show()
            elif Selected == "MoveFileDrives":
                CheckFlash()
                if not Flash_Drive == None:
                    shutil.move(FileSelected[0], (Flash_Drive))
                    FileSorter = "File"
                    Clearall()
                    draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                    draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                    draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                    draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                    IRFilesFunc(True)
                    show()
                else:
                    draw.text((10, 51), "Drive Not Inserted", font=ImageFont.load_default(), fill="#ffffff")
                    show()
                    time.sleep(1.5)
                    draw.text((10, 51), "Drive Not Inserted", font=ImageFont.load_default(), fill="#000000")
                    show()
            elif Selected == "MoveFileCancel":
                FileSorter = "File"
                Clearall()
                draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                IRFilesFunc(True)
                show()
            elif Selected == "DeleteFile":
                Clearall()
                draw.text((10, 3), "Delete File?", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((10, 16), "Yes", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((10, 27), "No", font=ImageFont.load_default(), fill="#ffffff")
                DeleteFileYes(True)
                show()
            elif Selected == "DeleteFileYes":
                os.remove(FileSelected[0])
                FileSorter = "File"
                Clearall()
                draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                IRFilesFunc(True)
                show()
            elif Selected == "DeleteFileNo":
                FileSorter = "File"
                Clearall()
                draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                IRFilesFunc(True)
                show()
            elif Selected == "RenameFile":
                Clearall()
                KeyBoardObject = ntpath.basename(FileSelected[0]).split(".")[0]
                CurrentKeyboardFocus = "FileRename"
                ShowKeyboard()
                draw.text((5, 2), "Name:", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((35, 2), KeyBoardObject, font=ImageFont.load_default(), fill="#ffffff")
                Keyboard_QBox(True)
                show()
            elif Selected == "FileSelectionBack":
                FileSorter = "File"
                Clearall()
                draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                IRFilesFunc(True)
                show()
            elif Selected == "FlashOk":
                FileSorter = "File"
                Clearall()
                draw.text((4, 48), "<-", font=ImageFont.load_default(), fill="#ffffff")
                draw.rectangle([(20, 0), (20, 64)], fill="#ffffff")
                draw.text((30, 3), "IR", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((30, 18), "Bad_USB", font=ImageFont.load_default(), fill="#ffffff")
                draw.text((30, 33), "Drives", font=ImageFont.load_default(), fill="#ffffff")
                IRFilesFunc(True)
                show()
            time.sleep(0.1)
            
            
            
                
threading.Thread(target=ButtonEvents).start()
show()