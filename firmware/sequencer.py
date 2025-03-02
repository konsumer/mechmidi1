# this will eventually be main sequencer

from time import sleep
import board
import busio
from digitalio import Direction, DigitalInOut, Pull
from rotaryio import IncrementalEncoder
from keypad import KeyMatrix

import neopixel
import adafruit_ssd1306

# this just has pin definitions
from mechmidi1 import ROT0S,ROT0A,ROT0B,ROT1S,ROT1A,ROT1B,SDA,SCL,LED,ROW1,ROW2,ROW3,ROW4,ROW5,COL1,COL2,COL3,COL4

# setup RGB LEDs
pixels = neopixel.NeoPixel(
    LED,
    20,
    brightness=0.1,
    auto_write=False,
    pixel_order=neopixel.GRB
)

# setup i2c and OLED
i2c = busio.I2C(SCL, SDA, frequency=1_000_000)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
display.rotation=2

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



display.fill(0)
display.show()
display.text("SORRY!", 0, 0, 1)
display.text("I am still", 0, 10, 1)
display.text("working on this.", 0, 20, 1)
display.show()