
class RythmPattern:
	def __init__(self, categories, durations, holds=None):
		if holds == None:
			holds = durations
		self.categories = categories
		self.durations = durations
		self.holds = holds
		assert(sum(durations) % 4 < 0.05) # integer measures
		
	
	def get_measures_count(self):
		return sum(self.durations) / 4
	