import random
from note import Note

notes_seq = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
notes_eq = {"Bb" : "A#", "Db" : "C#", "Eb" : "D#", "Gb" : "F#", "Ab" : "G#"}

def cycle(array, times, callback, mode=0):
	# 0 Ascending
	# 1 descending
	# 2 ascending then descending
	# 3 descending then ascending
	if mode == 0:
		j = 0
		for i in range(0, times):
			callback(array[j])
			j = (j+1)%len(array)
	elif mode == 1:
		j = len(array) - 1
		for i in range(0, times):
			callback(array[j])
			j = j - 1 if j > 0 else len(array) - 1
	elif mode >= 2:
		j = 0
		reverse = mode == 3
		for i in range(0, times):
			callback(array[j])
			if reverse:
				j -= 1
				reverse = j != 0
			else:
				j += 1
				reverse = j == len(array) - 1
		
		
		
def equivalent(note):
	for key in notes_eq:
		if key == note.name:
			note = Note(notes_eq[key], note.octave)
	return note
	
def shift_semitone(note, shift):
	assert(abs(shift) < 12)
	
	note = equivalent(note)
	
	i = notes_seq.index(note.name) + shift
	octave = note.octave
	if i < 0:
		i += len(notes_seq)
		octave -= 1
	elif i >= len(notes_seq):
		i -= len(notes_seq)
		octave += 1
		
	return Note(notes_seq[i], octave)