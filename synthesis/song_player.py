import pygame
import threading
import time
import numpy
from constants import SAMPLE_RATE   
class SongPlayer:
    def __init__(self):
        self.thread = None
        self.ch = pygame.mixer.find_channel()
        self.snd = None
        
        
    def play(self, song):
        gen = song.generate()
        arr = numpy.array(gen, dtype="int16")
        duration = float(len(arr)) / SAMPLE_RATE
        snd = pygame.sndarray.make_sound(arr)
        def play_it():
            while self.ch.get_busy():
                time.sleep(0.000000001)
            self.ch.play(snd)
        
        if self.thread != None:
            self.thread.join()
            
        self.thread = threading.Thread(target=play_it)
        self.thread.start()
        return gen
        
    def play_override(self, song):
        gen = song.generate()
        arr = numpy.array(gen, dtype="int16")
        duration = float(len(arr)) / SAMPLE_RATE
        snd = pygame.sndarray.make_sound(arr)
        def play_it():
            if self.snd != None:
                self.snd.stop()
            self.snd = snd
            
            self.ch.play(snd)
       
        play_it()
        return gen