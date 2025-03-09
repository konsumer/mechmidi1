from time import sleep, monotonic_ns
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
import adafruit_midi
import usb_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange
from adafruit_midi.program_change import ProgramChange
from adafruit_midi.system_exclusive import SystemExclusive
import saminfo
from mechmidi1 import Menu,ROT0S,ROT0A,ROT0B,ROT1S,ROT1A,ROT1B,SDA,SCL,LED,ROW1,ROW2,ROW3,ROW4,ROW5,COL1,COL2,COL3,COL4,TX

### setup

# setup USB midi on all channels
midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0] )

# this is for SAM2695 on TX
uart = busio.UART(tx=TX, baudrate=31250, bits=8, parity=None, stop=1)
sam = adafruit_midi.MIDI(midi_out=uart, out_channel=0)
sam.send(SystemExclusive([0x7e, 0x7f], [0x09, 0x01])) # Reset
sam.send(SystemExclusive([0x7f, 0x7f, 0x04], [0x01, 0x00, 123 & 0x7f])) # Volume 123

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
      sleep(1)
      logo.hidden = True

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

### /setup


instruments = []
def instruments_load():
  # initially just set instrument 0-F to 0-F patch
  for i in range(16):
    instruments.append((saminfo.patches[i], i))
  try:
    with open("instruments.txt") as f:
      for line in f.readlines():
        (c,p) = line.strip().split(':')
        if c and p:
          i = int('0x' + p)
          instruments[int('0x' + c)] = (saminfo.patches[i], i)
  except:
    pass




# TODO: check if we can save (normally we can't, if CIRCUITPYTHON is mounted)
def instruments_save(channel, patch):
  t.text=f"To persist:\nadd {hstring(channel)}:{hstring(patch)} in instruments.txt"
  sleep(3)

# convert number to nice hex
def hstring(n):
  return hex(n).replace('0x', '').upper()


# initial song-loading is a bit jenk, but I will add more, later
from songs import aaaaaa as song
current_pattern = 0
current_instrument = 0
song_position = 0
pattern_position = 0
song_playing = True
function_buttons = [0,0,0,0]

play_on_press = True

# simple drum machine
def drum_machine():
  global current_instrument
  global current_pattern
  global song
  global song_playing

  rot[0].position = song.bpm

  pixels.fill(BLACK)
  pixels.show()
  running = True
  t.text = f"BPM: {song.bpm}\n{saminfo.drum_names[current_instrument]}"
  
  pixels.fill(BLACK)
  pixels[16] = (0x30, 0x30, 0x30)
  pixels[17] = (0x10, 0x30, 0x30)
  pixels[18] = (0x30, 0x10, 0x30)
  pixels[19] = (0x30, 0x30, 0x10)

  position = 0
  start_time = monotonic_ns()
  
  while running:
    song.bpm = rot[0].position
    seconds_per_beat = 15_000_000_000 / song.bpm
    
    for i,v in enumerate(song.beat_patterns[current_pattern][current_instrument]):
      if v:
        pixels[i] = RAINBOW[current_instrument % len(RAINBOW)]
      else:
         pixels[i] = BLACK
    e = keys.events.get()
    if e:
      if e.key_number > 15:
        k = e.key_number - 16
        if e.pressed:
          function_buttons[k] = 1
        else:
          function_buttons[k] = 0
      else:
        if function_buttons[0] & e.pressed:
          current_instrument = e.key_number
        else:
          if e.pressed:
            if play_on_press:
              sam.send(NoteOn(note=current_instrument+35, velocity=100), channel=9)
            if song.beat_patterns[current_pattern][current_instrument][e.key_number]:
              song.beat_patterns[current_pattern][current_instrument][e.key_number] = 0
            else:
              song.beat_patterns[current_pattern][current_instrument][e.key_number] = 1

    if function_buttons[0]:
      t.text = f"BPM: {song.bpm}\n{saminfo.drum_names[current_instrument]}\nChoose Instrument"
    else:
      t.text = f"BPM: {song.bpm}\n{saminfo.drum_names[current_instrument]}"

    if song_playing:
      ct = monotonic_ns()
      if (ct - start_time) > seconds_per_beat:
        start_time = ct
        position = (position + 1) % 16
        for i,v in enumerate(song.beat_patterns[current_pattern]):
          if v[position]:
            sam.send(NoteOn(note=i+35, velocity=127), channel=9)

      pixels[position] = (60, 60, 60)

    if not rotb[0].value:
      running = False

    pixels.show()
  pixels.fill(BLACK)
  pixels.show()
  sleep(0.2)
  currentMode = MenuMain(t, rot[0], rotb[0])



class MenuChooseInstrument(Menu):
  def __init__(self, channelnum, textArea, rot, button):
    items = []
    for i,v in enumerate(saminfo.patches):
      items.append(f"{hstring(i)} {v}")
    items.append("<- Back")
    self.channelnum = channelnum
    super(MenuInstruments, self).__init__(f"Channel {hstring(channelnum)}", items, textArea, rot, button)
    self.rot.position = instruments[channelnum][1]
    self.oldpos = -1
  
  def select(self, position):
    global currentMode
    pixels.fill(BLACK)
    pixels.show()
    sleep(0.2)
    if position != 128:
      instruments[self.channelnum] = (saminfo.patches[position], position)
      instruments_save(self.channelnum, position)
    currentMode = MenuInstruments(self.t, self.rot, self.button)

  # let user play instrument when they are choosing
  def show(self):
    super(MenuInstruments, self).show()
    position = self.rot.position % len(self.items)
    if position < 128:
      if (position != self.oldpos):
        sam.send(ProgramChange(patch=position), channel=0)
        self.oldpos = position
      e = keys.events.get()
      if e and e.key_number < 16:
        if e.pressed:
          pixels[e.key_number] = RED
          sam.send(NoteOn(note=e.key_number+48, velocity=100), channel=0)
          pixels.show()
        else:
          pixels[e.key_number] = BLACK
          sam.send(NoteOff(note=e.key_number+48), channel=0)
          pixels.show()

class MenuInstruments(Menu):
  def __init__(self, textArea, rot, button):
    items = []
    for (i,v) in enumerate(instruments):
      items.append(f"{hstring(i)}:{hstring(v[1])} {v[0]}")
    items.append("<- Back")
    super(MenuInstruments, self).__init__("Instruments", items, textArea, rot, button)
    self.oldpos = -1
  
  def select(self, position):
    global currentMode
    pixels.fill(BLACK)
    pixels.show()
    sleep(0.2)
    if position == 16:
      currentMode = MenuSettings(self.t, self.rot, self.button)
    else:
      currentMode = MenuChooseInstrument(position, self.t, self.rot, self.button)

  # let user play instrument when they are choosing
  def show(self):
    super(MenuInstruments, self).show()
    position = self.rot.position % len(self.items)
    if position < 16:
      if (position != self.oldpos):
        sam.send(ProgramChange(patch=instruments[position][1]), channel=0)
        self.oldpos = position
      e = keys.events.get()
      if e and e.key_number < 16:
        if e.pressed:
          pixels[e.key_number] = RED
          sam.send(NoteOn(note=e.key_number+48, velocity=100), channel=0)
          pixels.show()
        else:
          pixels[e.key_number] = BLACK
          sam.send(NoteOff(note=e.key_number+48), channel=0)
          pixels.show()

class MenuSettings(Menu):
  def __init__(self, textArea, rot, button):
    super(MenuMain, self).__init__("Settings", ["Instruments", "<- Back"], textArea, rot, button)
  
  def select(self, position):
    global currentMode
    sleep(0.2)
    if position == 0:
      currentMode = MenuInstruments(self.t, self.rot, self.button)
    if position == 1:
      currentMode = MenuMain(self.t, self.rot, self.button)


class MenuMain(Menu):
  def __init__(self, textArea, rot, button):
    super(MenuMain, self).__init__("mechmidi", ["Beat", "Melody", "Settings"], textArea, rot, button)

  def select(self, position):
    global currentMode
    sleep(0.2)
    if position == 0:
      drum_machine()
    if position == 2:
      currentMode = MenuSettings(self.t, self.rot, self.button)


instruments_load()
logo_display()


currentMode = MenuMain(t, rot[0], rotb[0])
while True:
  currentMode.show()
