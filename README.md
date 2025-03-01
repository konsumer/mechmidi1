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
- solder remaining components on board. [this](https://learn.sparkfun.com/tutorials/how-to-solder-castellated-mounting-holes/all) was helpful for the RP2040-Zero
- if you want classic MIDI, connect a board, like [this](https://www.amazon.com/ubld-itTM-Breakout-Board-Multi-Voltage/dp/B0BYMC926Z) to "expansion port" on board. I did this as a seperate board because I had a MIDI breakout-board laying around and I wanted it all to fit on a very small main-board. Another trick is sometimes the MIDI ports are included with other features on the board. For example [this](https://shop.m5stack.com/products/midi-unit-with-din-connector-sam2695) has MIDI DIN IN/OUT, as well as TRS MIDI ports, and has a full sound-engine built in (entire General Midi of 127 decent-sounding instruments.) Even if you don't want the sounds, the MIDI connections alone are useful, but with sounds, it makes the device even cooler!
- [install circuitpython](https://circuitpython.org/board/waveshare_rp2040_zero/) and any [libs](https://circuitpython.org/libraries) you need to RP2040 (I generally just start with a bundle.) You can skip this if you want arduino or some other firmware, but circuitpython is recommended initially, to test things, easily.

### expansion & hardware

At the top-left of board, there is an expansion port for MIDI/serial/i2c/power.

<img width="595" alt="ports" src="https://github.com/user-attachments/assets/48e9c05e-9328-4980-88ad-a80fd341e647" />

```
[GND] (3V3) (TX) (RX) (SCL) (SDA)
```

Use this to hook up classic midi daughter-board, or any other i2c/serial thing you want.

If you need to access these pins in code or want to expand the board, here is how they are hooked up to the RP2040-Zero:

<img width="621" alt="pinout" src="https://github.com/user-attachments/assets/d24afc06-6173-474e-ba84-84b27f598f73" />

- `VCC` (3.3V) and `GND` are power. I did not expose `5V`, but you could add it to expansion-port, or you can just add a bodge-wire to chip-pin or one of the through-holes on board, if you need that. IO is best at `3.3V` for this chip, so I wanted to keep it all "easy to stay safe"
- `LED` is a neopixel-line (has 20 RGB LEDs on it, but you can add many more.) Again, a bodge-wire will be needed to add more pixels to this line, but it's fairly easy to solder one on, if you need that.
- `COL(X)`/`ROW(X)` are the keyboard-matrix
- `ROT(X)A`/`ROT(X)B`/`ROT(X)S` are the rotary-encoders (`S` is the push-down switch)
- `SDA`/`SCL` is i2c. You can add up to 127 devices to this bus (each has it's own address, and they share wires) but OLED takes up 1 slot
- `RX`/`TX` is serial or classic MIDI (with a little circuit)

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
