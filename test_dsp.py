from math import sin, pi

freq = 220
sec = 2
rate = 8000
w = [chr(127 + int (127*sin(i * 2 * pi * freq/rate))) for i in xrange(rate)]*sec
s = ''.join(w)
print s
