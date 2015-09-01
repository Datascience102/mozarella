import random
from note import Note, Chord

class MelodicPattern:
	def __init__(self, categories, pattern):
		self.categories = categories
		self.pattern = pattern
	
	def generate(self, startnote, scale, notes_count):
		assert(isinstance(startnote, Note) or isinstance(startnote, Chord))
		notes = []
		note = startnote
		for i in range(0, notes_count):
			j = i % len(self.pattern)
			func = self.pattern[j]
			next_notes = func(scale, note)
			notes += next_notes
			note = next_notes[-1]
		return notes
		
# Patterns
def pnote_shift(n=1):
	# Note shift in a scale
	def f(scale, note):
		return [scale.shift(note, n)]
	return f
	
def pnote_shift_range(mini=-2, maxi=2):
	n = random.randint(mini, maxi)
	# Note shift in a scale
	def f(scale, note):
		return [scale.shift(note, n)]
	return f

def pnote_repeat():
	def f(scale, note):
		return [note]
	return f
	
def pnote_octave_shift(n):
	def f(scale, note):
		return [Note(note.name, note.octave+n)]
	return f
	
def pnote_any(min_octave=4, max_octave=-1):
	octave = min_octave
	if max_octave != -1:
		octave = random.randint(min_octave, max_octave)
		
	def f(scale, note):
		return [Note(random.choice(scale.notes), octave)]
	return f

def pchord_previous():
	def f(scale, note):
		return [scale.generate_chord(0, note)]
	return f

def pat_repeat(pattern, times=4):
	def f(scale, note):
		pat = MelodicPattern(None, pattern)
		notes = pat.generate(note, scale, times)
		return notes
	return f

def pat_ternary(pnote1, pnote2, flavour=0):
	def f(scale, note):
		pat1 = MelodicPattern(None, [pnote1])
		pat2 = MelodicPattern(None, [pnote2])
		notes1 = pat1.generate(note, scale, 1)
		note1 = notes1[0]
		note2 = pat2.generate(notes1[-1], scale, 1)[0]
		if flavour == 0:
			return [note1, note1, note2, note1, note1, note2, note1, note2]
		else:
			return [note2, note1, note1, note2, note1, note1, note2, note1]
	return f

full_random = MelodicPattern(["Melody"], [pnote_any(1, 4)])
randoshift = MelodicPattern(["Melody"], [pnote_any(1, 4), pnote_shift_range(-2),
			  pnote_shift_range(-2), pnote_shift_range(-2),
			  pnote_shift_range(-2), pnote_shift_range(-2),
			  pnote_shift_range(-2), pnote_shift_range(-2)])

melo1 = MelodicPattern(["Melody"], 
	    [
			pnote_any(1, 4),
			pat_repeat([
				pnote_octave_shift(1),
				pnote_octave_shift(-1),
			], 4)
		])
ternary = MelodicPattern(["Rythm", "Melody", "Ternary"],
	    [
			pat_ternary(pnote_octave_shift(-1), pchord_previous(), 1)
		])
ternary2 = MelodicPattern(["Rythm", "Melody", "Ternary"],
	    [
			pat_ternary(pnote_shift_range(-3, -3), pnote_octave_shift(1), 1)
		])
all_melodic_patterns = [
	full_random, randoshift, melo1, ternary2]