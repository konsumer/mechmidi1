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

from adafruit_led_animation.color import RAINBOW, RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA, WHITE, BLACK, GOLD, PINK, AQUA, JADE, AMBER, OLD_LACE
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.sparklepulse import SparklePulse

import adafruit_displayio_ssd1306

from mechmidi1 import Menu,ROT0S,ROT0A,ROT0B,ROT1S,ROT1A,ROT1B,SDA,SCL,LED,ROW1,ROW2,ROW3,ROW4,ROW5,COL1,COL2,COL3,COL4

# setup i2c and OLED
displayio.release_displays()
i2c = busio.I2C(SCL, SDA, frequency=1_000_000)
display = adafruit_displayio_ssd1306.SSD1306(I2CDisplayBus(i2c, device_address=0x3C), width=128, height=64, rotation=180)

screen = displayio.Group()
display.root_group = screen

# display logo
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
    brightness=0.2,
    auto_write=False,
    pixel_order=neopixel.GRB
)
pixels.fill(0)
pixels.show()

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

# setup text-display
t = label.Label(terminalio.FONT, text="", color=0xffffff, x=0, y=5)
screen.append(t)


t.text = "I am still\nworking\non this."
while True:
  pass
