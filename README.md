This is a [RP2040-Zero](https://www.waveshare.com/rp2040-zero.htm) mechanical keyboard I designed to be a MIDI controller/sequencer and/or macro-keypad. It's made to be highly configurable & easy to modify.

> [!CAUTION]
> After assembling, I think the keys are a tiny bit too close together (spacing left/right should be doubled) and I think the RP2040 needs a board-cutout to make it lay flush. You can solder it as it is, but it makes it much harder, because it has a gap between the boards. It's pretty expensive to iterate (buying assembled boards in bulk) so I will probly not modify/test updates to the design, but if I were making more, I would space the keys out more and cut a square under the RP2040.

## Features

- 20-key keypad with MX-style switches
- OLED 128x64 display
- 2 rotary encoders (each with a button)
- 20 RGB LEDs
- i2c port for adding more stuff (for example I might make a dongle for bluetooth or USB midi/keyboard/mouse/gamepad host)
- old-school MIDI in/out
- I used pi 2040, but you can use any chip, with a little modification
- designed to be easy to reflow-solder with a toaster oven, if you are manufacturing/assembling yourself
- Fully programmable with [CircuitPython](https://circuitpython.org/)
- Use [KMK](https://github.com/KMKfw/kmk_firmware) for a more keyboard-focused python-programmable firmware
- Use MIDI-focused firmware over USB, or with oldschool MIDI-out, that does sequencing
- translate USB MIDI to oldschool MIDI (no USB host, but it can interact with computer)
- pattern/song/track sequencer for sequencing drums
- pattern/song/track sequencer for sequencing notes
- arpeggio sequencer

## build/install

- order PCB & parts. Feel free to use whatever cheaper parts you can find. It pays to look around, especially with the OLED and LED chips. The key-switches are also totally up to you, but I recommend something clear, so the light shines through better. You will also need keycaps (again, clear or matte white looks nice)
- if you want to use easyeda & [jlcpcb](https://jlcpcb.com/) (it's very cheap & easy) you can disable any parts you don't need/want in BOM, and it will leave them out. For example, I didn't use the keys or 2040 they listed, I used my own (and it ended up better, I think.)
- solder remaining components on board. [this](https://learn.sparkfun.com/tutorials/how-to-solder-castellated-mounting-holes/all) was helpful for the RP2040-Zero. Flux really helps, and a cheap USB microscope, if you have one. Basically, I fluxed it up, put a pointy tipped iron in slot, then added a lil solder, for each pin.
- if you want classic MIDI, connect a board, like [this](https://www.amazon.com/ubld-itTM-Breakout-Board-Multi-Voltage/dp/B0BYMC926Z) to "expansion port" on board. I did this as a seperate board because I had a MIDI breakout-board laying around and I wanted it all to fit on a very small main-board. Another trick is sometimes the MIDI ports are included with other features on the board. For example [this](https://shop.m5stack.com/products/midi-unit-with-din-connector-sam2695) has MIDI DIN IN/OUT, as well as TRS MIDI ports, and has a full sound-engine built in (entire General Midi of 127 decent-sounding instruments.) Even if you don't want the sounds, the MIDI connections alone are useful, but with sounds, it makes the device even cooler!
- [install circuitpython](https://circuitpython.org/board/waveshare_rp2040_zero/) and any [libs](https://circuitpython.org/libraries) you need to "circuitpython" disk, in lib dir. You can skip this if you want arduino or some other firmware, but circuitpython is recommended initially, to test things, easily. For me, the whole circuitpython bundle was too big, so just copy [firmware](firmware). My code.py is meant to test each part initially (so youc an make sure hardware/software is setup right.)
- move sequencer.py to code.py, and reboot, and you should have a complete device.

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

### cost

You can definitely find these cheaper, if you look around. Although it's cheaper than any nice MIDI controller/sequencer/synth I found, that did what I want, super-cheap was not really a goal for me, with this project. It could be done differently, and much cheaper, I just wanted everything to work just like this, and be pretty quick/easy to assemble (it's a gift for a young-person, with not too much soldering experience.)

If you do it all my way, the per-unit cost is about $40, not including addons or whatever. A [nice midi & sound addon](https://shop.m5stack.com/products/midi-unit-with-din-connector-sam2695) is another $15.

- board with assembly - a bit cheaper in bulk, with assembly. I ordered 10, at $16 each (including shipping) and it has most of the parts on the board (no RP2040 or keys.) In much larger quantites, the price goes way down, and you can shop around for cheapest board (I went with easiest.) I can sell you a pre-populated board for $16 (not including shipping to you) until I run out. I currently have 5 of these on-hand. You can also get the price down by etching/assembling yourself, and just ordering parts (in bulk) but some of the parts are a bit tricky to solder by hand (a toaster would work better for the LEDs and diodes.) $16 seems pretty cheap to me, and the hardest soldering is done, and it's mostly all built, but some nice & fun soldering is left.
- RP2040-Zero - I bought [3 for $20](https://www.amazon.com/gp/product/B0BZ8D4CJM/?th) and got it the next day, but they are definitely way cheaper elsewhere (check aliexpress/etc) if you are willing to wait for shipping, especially if you are buying them in bulk (they are very useful for all kinds of things.)
- mech key switches - I used [these nice ones](https://www.amazon.com/gp/product/B0CDW74TX3), $20 for 45 (enough for 2 devices) but you can find these much cheaper.
- keycaps - I used [these](https://www.amazon.com/gp/product/B0CQ2XD4WT). $12 for 20, or $31 for 100. XDA is less "scuplted" than Cherry, but either will work fine.

To build 10, it's about $260 ($26 per unit):

- boards $160 - go cheaper by making your own, or printing/assembling more at a time. Assembly is not very expensive compared to the PCB, I have found, so it might be worth it to add $2 per-unit and save yourself some time/effort.
- key switches $84 - you can definitely find these cheaper on aliexpress
- [10 2040s](https://www.aliexpress.us/item/3256806922860079.html) $15
- order some super-cheap keycaps that will work for you. clear is best, but white will work fine, too. If you are ok with lettering on them, you can reuse a super-cheap macropad-set.

You could get this even cheaper with greater bulk-quantities, and shopping around, though.

### ideas for cheaper

- Use membrane-keys (silicone buttons over PCB traces) instead of mech-keys
- drop LEDs, or use single-color
- drop OLED
- drop rotary-encoders
- try to get all parts on single-side (for cheaper/easier-to-make-at-home PCB)

## Modify

This thing is meant to be hacked!

### hardware

- Install [EasyEDA](https://easyeda.com/)
- move things in schematice however you want, or add/remove anyhting you like. Make sure to update PCB (alt-I.) The 2040 is maxed-out for GPIO, but the layout should be simple enough to modify (unroute all, then do your business with nets like `COL0`, `ROW0`, etc, then auto-route.) I recommend replacing the chip wityh somerthing bigger if you want to do ther stuff (see [picoadk](https://www.tindie.com/products/datanoisetv/picoadk-audio-development-kit-raspberry-rp2040/) for a nice 2040 firmware for larger pico, with sound-generatin in mind!)

> [!NOTE]
> I ended up recreating/improving project in EasyEDA because it was easier with [jlcpcb](https://jlcpcb.com/), which is pretty cheap for making the PCB and assembly. This means the [kicad stuff](kicad) is not totally up-to-date, but I left it, if anyone is interested. It should still work, but it's not tested, and it's layed-out a bit differently.

### software

If you want to change how the software works, I have created a [simple lib](firmware/midimech1.py) to interact with the existing hardware in [CircuitPython](https://circuitpython.org/). See how I use it in [sequencer.py](firmware/sequencer.py). If you chnage the hardware, you will probly need to also modify these.

### TODO

- I need to actually create the sequencers and stuff
- [SAM](https://docs.dream.fr/pdf/Serie2000/SAM_Datasheets/SAM2695.pdf) chip can do a ton of stuff, demos should use effects and things
