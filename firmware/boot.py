import supervisor
import usb_hid
import usb_midi 

# disable writing REPL to OLED (not useful and ugly)
# it will still turn on if you break the loop
# this is just for initial boot
supervisor.status_bar.display = False
supervisor.status_bar.console = False
display.root_group = None

# disable acting as HID device, enable USB MIDI
usb_hid.disable()
usb_midi.enable()