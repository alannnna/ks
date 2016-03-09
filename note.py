# From https://gist.github.com/ohsqueezy/6540433

# Generate a 440 Hz square waveform in Pygame by building an array of samples and play
# it for 5 seconds.  Change the hard-coded 440 to another value to generate a different
# pitch.
#
# Run with the following command:
#   python pygame-play-tone.py

from array import array
from time import sleep
import pygame
from pygame.mixer import Sound, get_init, pre_init

from frequencies import midi_to_hz


N_OVERTONES = 15


class Note(Sound):

    def __init__(self, midi, volume=.1):
        self.midi = midi
        self.frequency = midi_to_hz(midi)
        Sound.__init__(self, buffer=self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        fundamental_period = int(round(get_init()[0] / self.frequency))
        samples = array("h", [0] * fundamental_period)

        for i in range(1, N_OVERTONES+1):
            period = int(round(get_init()[0] / (i * self.frequency)))
            amplitude = (2 ** (abs(get_init()[1]) - 1) - 1) / 4

            # Make the overtones quieter
            if i != 1:
                if i % 2 == 0:
                    amplitude /= i
                else:
                    amplitude /= i*4

            for time in xrange(fundamental_period):
                if time % period < period / 2:
                    samples[time] += amplitude
                else:
                    samples[time] += -amplitude
        return samples


if __name__ == "__main__":
    pre_init(44100, -16, 1, 1024)
    pygame.init()
    Note(440).play(-1)
    sleep(1)
    Note(220).play(-1)
    sleep(1)

