from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading
import time
import psutil
import os

##########################
#    MADE BY APROTONIX   #
##########################

SETTINGS_PATH =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.txt")

config = {}

try:
    with open(SETTINGS_PATH, "r") as f:
        exec(f.read(), {}, config)
except Exception as e:
    print("Error during loading settings : ", e)
    config = {
        "BG_COLOR": '#FFFFFF33',
        "COLORS": {"low": "#00B3FAB5", "warn": "#7700FFAA", "high": "#FF0000AA"},
        "SIZE": 64,
        "RADIUS": 15,
        "WARN_PERCENT": 70,
        "HIGH_PERCENT": 85
    }


BG_COLOR = config["BG_COLOR"]
COLORS = config["COLORS"]
SIZE = config["SIZE"]
RADIUS = config["RADIUS"]
WARN_PERCENT = config["WARN_PERCENT"]
HIGH_PERCENT = config["HIGH_PERCENT"]


def create_image(RAM):
    image = Image.new('RGBA', (SIZE, SIZE), BG_COLOR)
    draw = ImageDraw.Draw(image)
 
    #MASK
    mask = Image.new('L', (SIZE, SIZE), 0)
    mask_draw = ImageDraw.Draw(mask)
    #USAGE
    height = SIZE - (RAM / 100) * SIZE
    color = COLORS["low" if RAM < WARN_PERCENT else "high" if RAM > HIGH_PERCENT else "warn"]
    draw.rectangle([0, height, SIZE, SIZE], fill=color, outline=color)
    
    mask_draw.rounded_rectangle((0, 0, SIZE, SIZE), radius=RADIUS, fill=255)

    alpha = image.getchannel('A')
    new_alpha = Image.composite(alpha, mask, mask)
    image.putalpha(new_alpha)

    return image

def quit_app(icon, item):
    icon.stop() 
#MADE BY APROTONIX 
menu = Menu(
    MenuItem("Quit", quit_app),
    MenuItem("Settings", lambda: os.startfile(SETTINGS_PATH))
)

icon = Icon("RAM Usage", create_image(50), "RAM Usage", menu)

def animate_when_ready():
   
    while not icon.visible:
        time.sleep(0.1)
    
   
    while icon.visible:
        ram = psutil.virtual_memory().percent
        icon.title = f"RAM : {ram} %"
        icon.icon = create_image(ram)

        time.sleep(1)

threading.Thread(target=animate_when_ready, daemon=True).start()

icon.run()


