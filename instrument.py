#!/usr/bin/env python

from __future__ import division
# import RPi.GPIO as gpio
import pygame
from pygame.mixer import pre_init
from time import sleep

# from capsense import CapRead as cap_read
from note import Note
from chord_progression import get_next_chord, get_next_note


SENSOR_PIN = 17
OUT_PIN = 18


class TouchInstrument(object):
    def __init__(self):
        self.smooth_factor = 500
        self.max_notes = 16
        self.notes = []
        self.last_level = 0
        self.chord = 1
        self.key = 69  # Midi value for A4; key of A

    def get_sound_level(self):
        '''
        Returns an integer value for sound level, to be translated to
        chord complexity or something.
        '''
        total = 0
        for i in range(0, self.smooth_factor):
            total += cap_read(sensor_pin=SENSOR_PIN, out_pin=OUT_PIN)
        return max(total-4*self.smooth_factor, 0) // self.smooth_factor

    def add_note(self):
        print "adding note"

        if len(self.notes) == self.max_notes:
            return
        print self.notes
        notes = [note.midi for note in self.notes]
        print notes
        next_note = get_next_note(notes, self.chord, key=self.key)
        print next_note
        n = Note(next_note, volume=.05)
        n.play(-1)
        self.notes.append(n)

    def remove_note(self):
        print "removing note"

        try:
            n = self.notes.pop()
        except IndexError:
            return
        n.stop()
        if len(self.notes) == 0:
            self.chord = get_next_chord(self.chord)

    def set_sound(self, level):
        if level > self.last_level:
            for i in range(level - self.last_level):
                self.add_note()
        else:
            for i in range(self.last_level - level):
                self.remove_note()
        self.last_level = level

    def run(self):
        print "Starting TouchInstrument..."

        # rpi gpio setup
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        print "RPi GPIO initialized."

        # Sound setup (pygame)
        pre_init(44100, -16, 1, 1024)
        pygame.init()
        pygame.mixer.set_num_channels(self.max_notes)
        print "Sound initialized."
        print "TouchInstrument is ready."

        while True:
            level = self.get_sound_level()
            self.set_sound(level)

    def test_run(self):
        print "Starting TouchInstrument test..."

        # Sound setup (pygame)
        pre_init(44100, -16, 1, 1024)
        pygame.init()
        pygame.mixer.set_num_channels(self.max_notes)
        print "Sound initialized."

        levels = [0, 1, 2, 3, 4, 5, 4, 2, 1, 0, 0, 3, 6, 5, 4, 3, 1, 0, 1, 1, 0]
        counter = 0
        while True:
            self.set_sound(levels[counter])
            counter += 1
            if counter == len(levels):
                counter = 0
            sleep(0.5)


if __name__ == "__main__":
    ti = TouchInstrument()
    # ti.run()
    ti.test_run()
