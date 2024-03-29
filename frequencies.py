'''
Module for converting midi to Hz. There's some voodoo here with the
offset of freqencies from freqencies.txt and midi codes; please excuse.

TODO make general purpose for converting midi to hz to "A4"
'''
import os

def load_freqs():
    script_dir = os.path.dirname(__file__)
    rel_path = 'frequencies.txt'
    abs_path = os.path.join(script_dir, rel_path)

    with open(abs_path) as f:
        lines = f.readlines()
        # Ignore first line, it's metadata
        return [float(line.strip()) for line in lines[1:]]

FREQS = load_freqs()
MIDI_MIN = 21  # Known based on freqs file
MIDI_MAX = 21 + len(FREQS) - 1  # Also known but laze

def midi_to_hz(midi):
    assert midi >= MIDI_MIN
    assert midi <= MIDI_MAX
    return FREQS[midi - 21]
