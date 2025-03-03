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

def logo_display():
  with open("logo.bmp", "rb") as logo_file:
    logo_bmp = displayio.OnDiskBitmap(logo_file)
    logo = displayio.TileGrid(
        logo_bmp,
        pixel_shader = getattr(logo_bmp, 'pixel_shader', displayio.ColorConverter()),
        x=25
    )
    screen.append(logo)
    display.refresh()
    # wait & hide logo
    sleep(1)
    logo.hidden = True

logo_display()

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

# setup text-display
t = label.Label(terminalio.FONT, text="", color=0xffffff, x=0, y=5)
screen.append(t)

###


def demo_input():
  while True:
    t.text = f"INPUT\nPress R0+R1 to exit\nR0: {rot[0].position} {not rotb[0].value}\nR1: {rot[1].position} {not rotb[1].value}"
    e = keys.events.get()
    if e:
        if e.pressed:
            pixels[e.key_number] = GREEN
        else:
            pixels[e.key_number] = BLUE
        pixels.show()
    if not rotb[0].value and not rotb[1].value:
      break
  pixels.fill(0)
  pixels.show()
  sleep(0.2)

# LED demos that wait for button-press

def demo_rainbow(button):
  pixels.brightness = 1
  rainbow = RainbowComet(pixels, speed=0.1, tail_length=8, bounce=True)
  t.text = "Live in full color,\nand you'll find the\nrainbow in every\nmoment."
  while button.value:
    rainbow.animate()
  pixels.fill(0)
  pixels.show()
  pixels.brightness = 0.2
  sleep(0.2)

def demo_satan(button):
  pixels.brightness = 1
  t.text = "\n" + "Praise Satan!!!!".center(20)
  p=SparklePulse(pixels, speed=0.1, breath=0.05, color=RED)
  while button.value:
    p.animate()
  pixels.fill(0)
  pixels.show()
  pixels.brightness = 0.2
  sleep(0.2)

def demo_cop(button):
  pixels.brightness = 1
  t.text = "\n".join([
    "All".center(20),
    "Cops".center(20),
    "Are".center(20),
    "Bastards".center(20)
  ])
  c = RED
  while button.value:
    if c == RED:
      c = BLUE
    else:
      c = RED
    pixels.fill(c)
    pixels.show()
    sleep(0.1)
  pixels.fill(0)
  pixels.show()
  pixels.brightness = 0.2
  sleep(0.2)

class MenuLED(Menu):
  def __init__(self, textArea, rot, button):
    super(MenuLED, self).__init__("LED Demos", ["Rainbow", "Satan", "Pigs", "<- Back"], textArea, rot, button)

  def select(self, position):
    global currentMode
    sleep(0.2)
    self.doselect = True
    if position == 0:
      demo_rainbow(self.button)
    if position == 1:
      demo_satan(self.button)
    if position == 2:
      demo_cop(self.button)
    if position == 3:
      currentMode = MenuDemos(self.t, self.rot, self.button)
    else:
      currentMode = MenuLED(self.t, self.rot, self.button)

class MenuDemos(Menu):
  def __init__(self, textArea, rot, button):
    super(MenuDemos, self).__init__("Demos", ["LEDs", "Input", "Logo"], textArea, rot, button)

  def select(self, position):
    global currentMode
    sleep(0.2)
    self.doselect = True
    if position == 0:
      currentMode = MenuLED(self.t, self.rot, self.button)
    if position == 1:
      demo_input()
    if position == 2:
      self.t.text = ""
      logo_display()

currentMode = MenuDemos(t, rot[0], rotb[0])

while True:
  keys.events.get()
  currentMode.show()
