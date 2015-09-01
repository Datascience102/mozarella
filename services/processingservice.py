import numpy
import time
import pygame
OK_THRESH = 80000 #11000
class ProcessingService:
    def __init__(self, **kwargs):
        self.threshold = kwargs.get('threshold', OK_THRESH)
        self.sustain = False
        self.last_beat = 0
        self.t_s = time.clock()
        self.t = 0
        self.bpm = 0
        self.beat = False
        
    def process(self, chunk, dt):
        now = pygame.time.get_ticks() / 1000.0
        
        chunk = [-numpy.abs(c) for c in numpy.fft.fft(chunk)]
        chunk_size = len(chunk)
        
        # Selection des basses
        bass = chunk[3*chunk_size/4:4*chunk_size/4]
        bass_avg = numpy.average([abs(v) for v in bass])
        tap = False
        beat = False
        if abs(bass_avg) > self.threshold:
            tap = True
            # Calcule les BPM
            if not self.sustain:
                beatduration = 60 * 1 / (now - self.last_beat)
                print now, beatduration, now - self.last_beat
                self.last_beat = now
                if beatduration < 240:
                    self.bpm = (beatduration + self.bpm * 3)/4
                    beat = True
                self.sustain = True
                # print "yay", bass_avg
        else:
            self.sustain = False
            
        self.t += chunk_size
        self.t_s = now
        return (chunk, self.bpm, tap, beat)