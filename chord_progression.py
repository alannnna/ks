'''
Chord progressions based on this image:
http://www.electricchili.com/wp-content/uploads/2010/06/ScreenHunter_13-Jun.-20-08.47.jpg

TODO should probably write a class Chord
'''
from __future__ import division
from random import choice, randint

from note import Note
from frequencies import MIDI_MAX, MIDI_MIN

# Number of half-step differences between notes in each chord
CHORDS = {
	'maj': [0, 4, 7],
	'min': [0, 3, 7],
	'dim': [0, 3, 6],
	'7'  : [0, 4, 7, 10],
}
MAJOR_QUALITIES = ['maj', 'min', 'min', 'maj', '7', 'min', 'dim']
MAJOR_PROGRESSION = {
	3: [6],
	6: [2, 4],
	2: [5, 7],
	4: [5, 7],
	5: [1],
	7: [1],
	1: [3, 6, 2, 4, 5, 7]
}
OCTAVE_SIZE = 12


def get_next_chord(curr):
	return choice(MAJOR_PROGRESSION[curr])


def get_next_note(notes, chord, key=69):
	''' Returns midi note that would be okay to add to the current chord '''
	assert chord in range(1,8)
	assert key in range(MIDI_MIN, MIDI_MAX-OCTAVE_SIZE)

	chord_qual = MAJOR_QUALITIES[chord-1]

	print "getting next note for chord {0}, quality {1}".format(chord, chord_qual)

	if not notes:
		# Return the root of the desired chord in whatever key
		return key + chord-1

	# Add the next chord value in the sequence
	offset = CHORDS[chord_qual][len(notes)%len(CHORDS[chord_qual])]

	# Set an octave offset
	if len(notes)%len(CHORDS[chord_qual]) == 1 or randint(0, 1):
		octave_offset = -1 * (len(notes) // len(CHORDS[chord_qual]))
	else:
		octave_offset = len(notes) // len(CHORDS[chord_qual])

	midi = key + chord-1 + offset + octave_offset*OCTAVE_SIZE

	# Make sure the note is in range; if it's not, choose a random octave for it.
	while (midi > MIDI_MAX) or (midi < MIDI_MIN):
		if midi > MIDI_MAX:
			midi -= randint(0, octave_offset - 1)
		elif midi < MIDI_MIN:
			midi += randint(0, -1*octave_offset - 1)

	return midi
