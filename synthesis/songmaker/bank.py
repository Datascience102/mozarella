import scales
import rythm_patterns
import patterns
class Bank:
	def __init__(self):
		self.scale_models = []
		self.rythm_patterns = []
		self.sections = []
		self.melodic_patterns = []
	
	def rythms_by_category(self, cat):
		return [rythm for rythm in self.rythm_patterns if cat in rythm.categories]
	
	def melodic_patterns_by_category(self, cat):
		return [rythm for rythm in self.melodic_patterns if cat in rythm.categories]

bank = Bank()
bank.scale_models += scales.all_scales
bank.rythm_patterns += rythm_patterns.all_rythms
bank.melodic_patterns += patterns.all_melodic_patterns