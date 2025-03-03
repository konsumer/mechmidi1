import board
from time import sleep

# hardware-GPIO for mechmidi1

ROW1=board.GP29
ROW2=board.GP28
ROW3=board.GP27
ROW4=board.GP26
ROW5=board.GP15

COL1=board.GP4
COL2=board.GP5
COL3=board.GP6
COL4=board.GP7

ROT0S=board.GP11
ROT0A=board.GP10
ROT0B=board.GP9

ROT1S=board.GP14
ROT1A=board.GP13
ROT1B=board.GP12

LED=board.GP8

TX=board.TX
RX=board.RX

SDA=board.GP2
SCL=board.GP3

# base-class for menu
class Menu:
  def __init__(self, title, items, textArea, rot, button):
    self.title = title
    self.items = items
    self.t = textArea
    self.rot = rot
    self.button = button
    self.lines=["","","",""]
    self.doselect = True
    rot.position = 0

  def show(self):
    position = self.rot.position % len(self.items)
    if not self.button.value and self.doselect:
      self.doselect = False
      self.select(position)
    i = [
      ("- " + self.title + " -").center(20),
      "  " + self.items[(position - 1) % len(self.items)],
      "> " + self.items[(position) % len(self.items)],
      "  " + self.items[(position + 1) % len(self.items)]
    ]
    self.t.text = "\n".join(i)

  def select(self, position):
    self.t.text = f"Chose {self.items[position]}"
    sleep(1)
    self.doselect = True
