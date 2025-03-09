import supervisor
import usb_hid
import usb_midi

# disable writing REPL to OLED (not useful and ugly)
# it will still turn on if you break the loop
# this is just for initial boot
supervisor.status_bar.display = False
supervisor.status_bar.console = False
display.root_group = None

# set the name, as it shows on host-OS
# these don't seem to actually work
supervisor.set_usb_identification("konsumer", "mechmidi")
usb_midi.set_names(
  streaming_interface_name="mechmidi",
  audio_control_interface_name="mechmidi",
  in_jack_name="mechmidi",
  out_jack_name="mechmidi"
)


# disable acting as HID device, enable USB MIDI
usb_hid.disable()
usb_midi.enable()
