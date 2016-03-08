from pyo import *
s = Server().boot()
f = Adsr(attack=.01, decay=.2, sustain=.5, release=.1, dur=5, mul=.5)
a = Sine(mul=f).out()
f.play()
s.gui(locals())