class Note:
	def __init__(self, name, octave):
		self.name = name
		self.octave = octave
	def __str__(self):
		return self.name + str(self.octave)
	def __repr__(self):
		return str(self)
class Chord:
	def __init__(self, notes):
		self.name = notes[0].name
		self.octave = notes[0].octave
		self.notes = notes
		
	def __str__(self):
		return "Chord:" + self.name + str(self.octave)
	def __repr__(self):
		return str(self)