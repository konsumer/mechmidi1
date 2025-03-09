# this is the initial pattern loaded into interface

# it's a bit wonky to set things up like this
# but circuitpython can't normally persist data
# so I can't really save these structures
# I think I need to check if it's connected to USB
# and set to R/W if not (so user can save things)

bpm = 60

# these are pattern numbers from below, for song-mode
melody = [0]
beat = [0]


# each line is an instrument
beat_patterns = [
  [
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0], # 0 Acoustic Bass Drum
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 1 Bass Drum 1
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 2 Side Stick
    [0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0], # 3 Acoustic Snare
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 4 Hand Clap
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 5 Electric Snare
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 6 Low Floor Tom
    [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1], # 7 Closed Hi Hat
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 8 High Floor Tom
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 9 Pedal Hi-Hat
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # A Low Tom
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # B Open Hi-Hat
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # C Low-Mid Tom
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # D Hi Mid Tom 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # E Crash Cymbal
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # F High Tom
  ]
]

# each line is an instrument
# if note is same as last, it stays on
# 0 is "no note"
melody_patterns = [
  [60, 60, 61, 61, 62, 62, 64, 64, 65, 65, 67, 67, 69, 69, 72, 72],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
]
