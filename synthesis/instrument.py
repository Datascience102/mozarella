import math
import oscillators
from synthesis.constants import *


class Instrument(object):
    def __init__(self, **kwargs):
        pass
    
    def get_sample(self, note, octave, volume, start_sampletime, sampletime, end_sample):
        return 0
        
class Delay(Instrument):
    def __init__(self, inst, delay):
        self.delay = delay
        self.inst = inst
        
    def get_sample(self, note, octave, volume, start, t, end):
        s1 = self.inst.get_sample(note, octave, volume, start, t, end)
        s2 = self.inst.get_sample(note, octave, volume, start, t-self.delay, end)*0.5
        return s1+s2
        
class ADSREnvelope(Instrument):
    def __init__(self, inst, attack, decay, sustain, release, attack_peak=1.0, decay_descent=0.5):
        self.inst = inst
        self.attack_peak = attack_peak
        self.decay_descent = decay_descent
        self.sustain = sustain
        self.release = release
        self.attack = attack
        self.decay = decay
    
    def adsr(self, time, duration):
        percent = time / float(duration)
        if percent <= self.attack:
            return self.attack_peak * percent / self.attack
        elif percent <= self.decay:
            corrected = percent - self.attack
            corrected_decay = self.decay - self.attack
            return self.attack_peak - self.decay_descent * (corrected / corrected_decay)
        elif percent <= self.sustain:
            return self.attack_peak - self.decay_descent
        elif percent <= self.release:
            corrected = percent - self.sustain
            corrected_release = self.release - self.sustain
            start = self.attack_peak - self.decay_descent
            return start - start * (corrected / corrected_release)
        else:
            return 0
           
    def get_sample(self, note, octave, volume, start, t, end):
        sample = self.inst.get_sample(note, octave, volume, start, t, end)
        envelope = self.adsr(t-start, end-start)
        return sample * envelope

class MultipleOscillator(Instrument):
    def __init__(self, spectrum, **kwargs):
        super(MultipleOscillator, self).__init__()
        self.spectrum = spectrum
        self.notes = {}
        self.oscillator = kwargs.get('oscillator', math.sin)
        self.sample_rate =  kwargs.get('sample_rate', SAMPLE_RATE)
        
    def compute_sample(self, note, octave, volume, start_sampletime, sample_time, end_sample):
        """
        volume : 0-100
        sample_time : time in samples
        """
        time_s = (sample_time - start_sampletime) / float(self.sample_rate)
        freq = FREQS[note] * (2 ** (octave-4))
        return int(volume * self.oscillator(freq * 2 * math.pi * time_s) * MAX_VALUE)
        
    def precompute_note(self, note, octave):
        if not note in self.notes:
            self.notes[note] = {}
        
        if not octave in self.notes[note]:
            chunk = []
            base_freq = FREQS[note] * OCTAVE_MULTIPLIERS[octave]
            chunk_period_s = 1.0 / base_freq
            chunk_size = int(self.sample_rate*chunk_period_s)
            print note, octave, chunk_size
            # Pour chaque sample
            for t in range(0, chunk_size):
                value = 0
                coefs = 0
                # Pour chaque "raie" de spectre
                for multiplier, volume, offset in self.spectrum:
                    #value += self.compute_sample(note, int(octave*multiplier), volume, 0, t+offset*chunk_size, chunk_size)
                    value += self.compute_sample(note, int(octave*multiplier), volume, 0, t*(1+offset), chunk_size)
                    coefs += volume
                    
                chunk.append(value/coefs)
                
            self.notes[note][octave] = chunk
            
        return self.notes[note][octave]
    
    def preload(self, notes, octaves):
        for note in notes:
            for octave in octaves:
                self.precompute_note(note, octave)
    
    def get_sample(self, note, octave, volume, start_sampletime, sampletime, end_sampletime):
        arr = self.precompute_note(note, octave)
        return arr[abs(sampletime-start_sampletime) % len(arr)] * volume