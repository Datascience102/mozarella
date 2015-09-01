import numpy
import pygame
from songmaker.note import Chord, Note
from constants import MAX_VALUE, SAMPLE_RATE
from core import settings

class Song:
    def __init__(self, bpm):
        self.bps = bpm / 60.0 * 4
        self.schedule = [] # tick_number, duration (ticks), inst, note, octave, volume
        self.min_duration = 0 # force song duration (min only)
        
    def add_note_old(self, tick_number, duration, inst, note, octave, volume):
        self.schedule.append((tick_number, duration, inst, note, octave, volume))
    
    def add_note(self, tick_number, duration, inst, note, volume):
        if isinstance(note, Chord):
            for n in note.notes:
                self.add_note(tick_number, duration, inst, n, volume)
        elif isinstance(note, Note):
            self.schedule.append((tick_number, duration, inst, note.name, note.octave, volume))
        else:
            raise Exception("Expected Note or Chord, got " + str(note))
        
    def __expandto(self, arr, index):
        if index < len(arr):
            return
        index = int(index)
        for i in range(len(arr), index+1):
            arr.append(0)
            
        
    def set_ticks(self, ticks):
        self.min_duration = (ticks / self.bps)

        
    def generate(self):
        inst_count = []
        arr = []
        self.__expandto(arr, self.min_duration * SAMPLE_RATE)
        for tick_number, duration, instrument, note, octave, volume in self.schedule:
            end = tick_number + duration
            samples_per_tick =  1.0 / self.bps * SAMPLE_RATE
            first_sample = int(samples_per_tick * tick_number)
            end_sample = int(samples_per_tick * end)
            
            # On joue la note
            self.__expandto(inst_count, end_sample)
            self.__expandto(arr, end_sample)
            
            for t in range(first_sample, end_sample):
                sample = instrument.get_sample(note, octave, volume, first_sample, t, end_sample)
                #print "vout", sample
                arr[t] += sample
                inst_count[t] += 1
                    
        n = max(inst_count)
        for t in range(0, len(arr)):
            arr[t] = max(-MAX_VALUE, min(MAX_VALUE, arr[t]))
            
        return arr
        
    def clear(self):
        self.schedule = []
        
    def play(self):
        arr = numpy.array(self.generate(), dtype="int16")
        snd = pygame.sndarray.make_sound(arr)
        ch = snd.play()
        while ch.get_busy():
            pygame.time.delay(1)