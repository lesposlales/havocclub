import piir
from piir.io import receive
from piir.decode import decode
from piir.prettify import prettify
import json
import time
import threading
from threading import Event
from gpiozero import LED
from gpiozero import Button
import os

StartReadButton = Button(24)
CancelReadDelete = Button(25)

PowerLED = LED(27)
ReadLED = LED(23)
ReadingLED = LED(22)


PowerLED.on()

keys = {}

event = Event()
active = None

def start():
    keys = {}
    ReadingLED.on()

    while True:
        data = decode(receive(17))
        if data:
            break
        if event.is_set():
            break
    if active:
        keys["Data1"] = data

        print(json.dumps(prettify(keys), indent=2))
        a=open("savedfile.json", "w")
        a.write(json.dumps(prettify(keys), indent=2))
        a.close()
        ReadingLED.off()
        ReadLED.on()

Readbuttonispres = False

def ButtonEvents():
    while True:
        global active
        
        if StartReadButton.is_pressed:
            global Readbuttonispres
            if Readbuttonispres == False:
                active = True
                Readbuttonispres = True
                thread = threading.Thread(target=start)
                thread.start()
            time.sleep(1)
                
        if CancelReadDelete.is_pressed:
            active = False
            Readbuttonispres = False
            ReadingLED.off()
            ReadLED.off()
            if os.path.exists("savedfile.json"):
                os.remove("savedfile.json")
            time.sleep(1)
                
threading.Thread(target=ButtonEvents).start()