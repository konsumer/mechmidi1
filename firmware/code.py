from time import sleep
import board
import busio
from digitalio import Direction, DigitalInOut, Pull
from rotaryio import IncrementalEncoder
from keypad import KeyMatrix
import neopixel
import displayio
import terminalio
from adafruit_display_text import label
from i2cdisplaybus import I2CDisplayBus

import adafruit_displayio_ssd1306

from mechmidi1 import ROT0S,ROT0A,ROT0B,ROT1S,ROT1A,ROT1B,SDA,SCL,LED,ROW1,ROW2,ROW3,ROW4,ROW5,COL1,COL2,COL3,COL4

# setup i2c and OLED
displayio.release_displays()
i2c = busio.I2C(SCL, SDA, frequency=1_000_000)
display = adafruit_displayio_ssd1306.SSD1306(I2CDisplayBus(i2c, device_address=0x3C), width=128, height=64, rotation=180)

screen = displayio.Group()
display.root_group = screen

with open("logo.bmp", "rb") as logo_file:
    logo_bmp = displayio.OnDiskBitmap(logo_file)
    logo = displayio.TileGrid(
        logo_bmp,
        pixel_shader = getattr(logo_bmp, 'pixel_shader', displayio.ColorConverter()),
        x=25
    )
    screen.append(logo)
    display.refresh()

# setup RGB LEDs
pixels = neopixel.NeoPixel(
    LED,
    20,
    brightness=0.1,
    auto_write=False,
    pixel_order=neopixel.GRB
)

# setup rotary-encoders
rot = [
    IncrementalEncoder(ROT0A, ROT0B, divisor=2),
    IncrementalEncoder(ROT1A, ROT1B, divisor=2)
]

rotb = [
    DigitalInOut(ROT0S),
    DigitalInOut(ROT1S)
]

rotb[0].direction=Direction.INPUT
rotb[0].pull=Pull.UP
rotb[1].direction=Direction.INPUT
rotb[1].pull=Pull.UP

# setup keypad
keys = KeyMatrix(row_pins=(ROW1,ROW2,ROW3,ROW4,ROW5), column_pins=(COL1,COL2,COL3,COL4))


# wait & hide logo
sleep(1)
logo.hidden = True

text_area = label.Label(terminalio.FONT, text="Hello.\nI'm going to run\nthrough some tests.", color=0xffffff, x=0, y=5)
screen.append(text_area)
sleep(2)
text_area.text = "TEST: RGB"

colors = (
    (255, 0, 0),   # red
    (0, 255, 0),   # green
    (0, 0, 255),   # blue
)
for c in range(3):
    pixels.fill(colors[c])
    pixels.show()
    sleep(1)
pixels.fill(0)
pixels.show()
pixels.fill(0)

while True:
    text_area.text = f"TEST: INPUT\nrot0: {rot[0].position} {not rotb[0].value}\nrot1: {rot[1].position} {not rotb[1].value}"
    e = keys.events.get()
    if e:
        if e.pressed:
            pixels[e.key_number] = colors[2]
        else:
            pixels[e.key_number] = colors[1]
        pixels.show()

