import math
import random
import oscillators
from instrument import MultipleOscillator
from synthesis.constants import *

class SnareSampler(MultipleOscillator):    
    def __init__(self, **kwargs):
        # TODO : propre
        # super(type(BasicInstrument), , **kwargs)
        self.spectrum = [(1, 1, 0)]
        self.notes = {}
        self.sample_rate =  kwargs.get('sample_rate', SAMPLE_RATE)
    
    def adsr(self, time, duration, attack, decay, sustain, release):
        # attack, decay, sustain, release
        attack_peak = 1.0
        decay_descent = 0.1
        percent = time / duration
        if percent <= attack:
            return attack_peak * percent / attack
        elif percent <= decay:
            corrected = percent - attack
            corrected_decay = decay - attack
            return attack_peak - decay_descent * (corrected / corrected_decay)
        elif percent <= sustain:
            return attack_peak - decay_descent
        elif percent <= release:
            corrected = percent - sustain
            corrected_release = release -sustain
            start = attack_peak - decay_descent
            return start - start * (corrected / corrected_release)
        else:
            return 0
        
        pass
    
    def compute_sample(self, note, octave, volume, start_sampletime, sample_time):
        """
        volume : 0-100
        sample_time : time in samples
        """
        print self.spectrum, note, octave
        if note == 'E':
            time_s = (sample_time - start_sampletime) / float(self.sample_rate)
            last_sample = 0.025
            vol = max(0, 1-time_s)
            val = 0
            
            for i in range(1, 10):
                pulse = 2 * math.pi * time_s * 0.5
                offset = pulse * i / 10
                vol /= i
                sin1 = math.sin(offset + pulse * 180)
                sin2 = math.sin(offset + pulse * 330) # 111
                tri1 = oscillators.triangle(offset + pulse * (111+175))
                tri2 = oscillators.triangle(offset + pulse * (111+224))
                val += vol * (sin1 + sin2 + tri1 + tri2) * MAX_VALUE / 4
            
            envelope = self.adsr(time_s, last_sample, 0.10, 0.15, 0.20, 1.0)
            noise = random.random() * MAX_VALUE / 8
            print time_s, envelope, vol
            return vol * math.sin(math.pi*time_s*440)* MAX_VALUE / 4# (val + noise) * envelope