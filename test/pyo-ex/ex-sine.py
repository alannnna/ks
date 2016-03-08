from pyo import *
s = Server(audio='coreaudio').boot()
s.start()
a = Sine(mul=0.01).out()
s.gui(locals())
