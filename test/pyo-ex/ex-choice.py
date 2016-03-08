from pyo import *
s = Server(audio='coreaudio').boot()
s.start()
freqs = midiToHz([60,62,64,65,67,69,71,72])
rnd = Choice(choice=freqs)
a = SineLoop(rnd, feedback=0.05, mul=.2).out()
s.gui(locals())
