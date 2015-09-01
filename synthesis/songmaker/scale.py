import random
from note import Note
from utils import *
from patterns import *	


		
class ScaleModel:
	def __init__(self, categories, semitones):
		if isinstance(semitones, str):
			semitones = [int(s) for s in list(semitones)]
		
		self.categories = categories
		self.semitones = semitones
		self.arpegios = []
		self.chords = []
	
	def add_arpegio(self, arpegio):
		"""
		arpegio: string ('1212121') with scale intervals or array
		"""
		if isinstance(arpegio, str):
			arpegio = [int(s) for s in list(arpegio)]
		self.arpegios.append(arpegio)
		
	def add_chord(self, chord):
		"""
		chord: string ('146') with scale intervals or array
		"""
		if isinstance(chord, str):
			chord = [int(s) for s in list(chord)]
		self.chords.append(chord)

class Scale:
	def __init__(self, model, dominant):
		self.dominant = dominant # dominant note. Ex. 'A'
		self.model = model
		self.notes = [] # string array
		current = Note(dominant, 4)
		for semitone in self.model.semitones:
			self.notes.append(current.name)
			current = shift_semitone(current, semitone)
	
	def shift(self, note, shift):
		note = equivalent(note)

		i = self.notes.index(note.name) + shift
		octave = note.octave
		if i < 0:
			while i < 0:
				i += len(self.notes)
			octave -= 1
		elif i >= len(self.notes):
			while i >= len(self.notes):
				i -= len(self.notes)
			octave += 1

		return Note(self.notes[i], octave)
	
	def generate_arpegio(self, arpegio_id, first_note, notes_count, mode=0):
		assert(first_note.name in self.notes)
		
		n = Note(first_note.name, first_note.octave)
		notes = [n]
		def callback(interval):
			n = self.shift(notes[len(notes)-1], interval)
			notes.append(n)
		cycle(self.model.arpegios[arpegio_id], notes_count-1, callback, mode)
		return notes

	def generate_chord(self, chord_id, first_note):
		"""
		Generates a chord
		returns: array of note-strings
		"""
		assert(isinstance(first_note, Note) or isinstance(first_note	, Chord))
		chord = self.model.chords[chord_id]
		note = Note(first_note.name, first_note.octave)
		notes = [note]
		for interval in chord:
			note = self.shift(note, interval)
			notes.append(note)
		
		return Chord(notes)
		
	def generate_chord_old(self, chord_id, first_note):		
		return self.generate_chord(chord_id, first_note).notes