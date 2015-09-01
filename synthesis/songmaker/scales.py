from scale import ScaleModel

base_arpegios = [
	"11111111", 
	[1, -2, 3], 
	[1, 2, -1], 
	[1, 1, 1, 1, -1, -1, -1, -1],
	[1, 2, -1, 1, -2, -1],
	[0, 0, 0, 0],
	[0, 1, 0, 1]
]

base_chords = [
	"7",
	"25"
]

def create_model(categories, semitones):
	model = ScaleModel(categories, semitones)
	for chord in base_chords:
		model.add_chord(chord)
	for arpegio in base_arpegios:
		model.add_arpegio(arpegio)
	return model


phrygian = create_model(["All"], "1312122")
algerian = create_model(["All"], "2131131")
chromatic = create_model(["All"], "111111111111")
dorian = create_model(["All"], "2122212")
blues = create_model(["All"], "321132")
all_scales = [
	phrygian,
	algerian,
	chromatic,
	dorian,
	blues
]