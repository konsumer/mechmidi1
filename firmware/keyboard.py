# This sets things up for KMK
# https://github.com/KMKfw/kmk_firmware

print("Starting KMK")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.RGB import RGB
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.extensions.display import Display, TextEntry
from kmk.scanners.encoder import RotaryioEncoder

keyboard = KMKKeyboard()

# TODO: configure for https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/keycodes.md
keyboard.keymap = [
    [KC.A,]
]
keyboard.debug_enable = True

keyboard.row_pins = (board.GP09,board.GP10,board.GP11,board.GP12,board.GP13)
keyboard.col_pins = (board.GP14,board.GP15,board.GP26,board.GP27)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# setup OLED
display = Display(
    display=SSD1306(sda=board.SDA, scl=board.SCL),
    entries=[TextEntry(text='Layer: ', x=0, y=32, y_anchor='B')]
    + [TextEntry(text=str(_), x=40, y=32, layer=_) for _ in range(9)],
    flip=True,
)
keyboard.extensions.append(display)

# setup first rotary
rotary = RotaryioEncoder(pin_a=board.GP04, pin_b=board.GP05)
keyboard.extensions.append(rotary)

# setup LEDs
rgb = RGB(pixel_pin=board.GP29, num_pixels=20)
keyboard.extensions.append(rgb)

if __name__ == '__main__':
    keyboard.go()
