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


# scan bus
i2c.try_lock()
print("i2c bus: ", end="")
print(i2c.scan())
i2c.unlock()

display.fill(0)
display.show()
display.text("This will test", 0, 0, 1)
display.text("various things.", 0, 10, 1)
display.text("first: LEDs.", 0, 20, 1)
display.text("You should", 0, 30, 1)
display.text("see R/G/B.", 0, 40, 1)
display.show()
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

display.fill(0)
display.text("Now: rotaries.", 0, 0, 1)
display.text("turn knobs", 0, 10, 1)
display.text("or press both to move on.", 0, 20, 1)
display.show()

while True:
    # TODO: just fill_rect(x,y,w,h,c)
    display.fill(0)
    display.text("Now: rotaries.", 0, 0, 1)
    display.text("turn knobs", 0, 10, 1)
    display.text("press both to end", 0, 20, 1)
    display.text(f"R0: {rot[0].position} {not rotb[0].value}   ", 0, 30, 1)
    display.text(f"R1: {rot[1].position} {not rotb[1].value}   ", 0, 40, 1)
    display.show()
    if not rotb[0].value and not rotb[1].value:
        break
    sleep(0.1)

display.fill(0)
display.text("Now: keypad.", 0, 0, 1)
display.text("press keys", 0, 10, 1)
display.text("see colors", 0, 20, 1)
display.show()

while True:
    e = keys.events.get()
    if e:
        if e.pressed:
            pixels[e.key_number] = colors[2]
        else:
            pixels[e.key_number] = colors[1]
        pixels.show()
