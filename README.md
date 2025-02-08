This is a [RP2040-Zero](https://www.waveshare.com/rp2040-zero.htm) mechanical keyboard I designed to be a MIDI controller/sequencer and/or macro-keypad. It's made to be highly configurable & easy to modify.

I am using some ideas from [here](https://www.youtube.com/watch?v=8WXpGTIbxlQ), and it needs testing (still in progress.)

> [!IMPORTANT]
> I eneded up recreating project in EasyEDA because it was easier with [jlcpcb](https://jlcpcb.com/), which is pretty cheap for making the PCB and assembly. Ordering 10, they cost me about $16 each, after shipping, even during supply-chain shortages, but I provided my own midi-out, keys & 2040. This means the kicad stuff is not totally up-to-date, but I left it, if anyone is interested.

## Features

- 20-key keypad with Cherry MX switches
- OLED 128x64 display
- 2 rotary encoders (each with a button)
- 20 RGB LEDs
- i2c port for adding more stuff onto it (for example I might make a dongle for bluetooth or USB midi/keyboard/mouse/gamepad host)
- old-school MIDI in/out
- I used pi 2040, but you can use any chip
- designed to be easy to reflow-solder with a toaster oven
- Fully programmable with [CircuitPython](https://circuitpython.org/)
- Use [KMK](https://github.com/KMKfw/kmk_firmware) for a more keyboard-focused firmware (programmable keyboard firmware)
- Use MIDI-focused firmware over USB, or with oldschool MIDI-out, that does sequencing
- translate USB MIDI to oldschool MIDI (no USB host, but it can interact with computer)
- pattern/song/track sequencer for sequencing drums
- pattern/song/track sequencer for sequencing notes
- arpeggio sequencer

## build/install

- order PCB & parts. Feel free to use whatever cheaper parts you can find. It pays to look around, especially with the OLED and LED chips. The key-switches are also totally up to you, but I recommend something clear, so the light shines through better. You will also need keycaps (again, clear looks nice)
- if you want to use easyeda & [jlcpcb](https://jlcpcb.com/) (it's very cheap & easy) you can disable any parts you don't need/want in BOM, and it will leave them out. For example, I didn't use the keys or 2040 they listed, I used my own (and it ended up better, I think.)
- solder remaining components on board.
- if you want oldschool MIDI, connect a board, like [this](https://www.amazon.com/ubld-itTM-Breakout-Board-Multi-Voltage/dp/B0BYMC926Z) to TX/RX on board (see schematic.) I did this as a seperae board because I had a MIDI breakout-board laying around and I wanted it all to fit on a very small main-board.
- [install circuitpython](https://circuitpython.org/board/waveshare_rp2040_zero/) and any [libs](https://circuitpython.org/libraries) you need to RP2040 (I generally just start with a bundle)

### MIDI sequencer/controller

- copy [midimech1.py](firmware/midimech1.py) to `lib/midimech1.py`
- copy [sequencer.py](firmware/sequencer.py) to `app.py`

### standard keyboard

- install [KMK](https://github.com/KMKfw/kmk_firmware)
- copy [keyboard.py](firmware/keyboard.py) (feel free to modify) to `app.py`


## Modify

This thing is meant to be hacked!


### hardware

- Install [EasyEDA](https://easyeda.com/)
- move things in schematice however you want, or add/remove anyhting you like. Make sure to update PCB (alt-I.) The 2040 is maxed-out for GPIO, but the layout should be simple enough to modify (unroute all, then do your business with nets like `COL0`, `ROW0`, etc, then auto-route.) I recommend replacing the chip wityh somerthing bigger if you want to do ther stuff (see [picoadk](https://www.tindie.com/products/datanoisetv/picoadk-audio-development-kit-raspberry-rp2040/) for a nice 2040 firmware for larger pico, with sound-generatin in mind!)

### software

If you want to change how the software works, I have created a [simple lib](firmware/midimech1.py) to interact with the existing hardware in [CircuitPython](https://circuitpython.org/). See how I use it in [sequencer.py](firmware/sequencer.py). If you chnage the hardware, you will probly need to also modify these.
