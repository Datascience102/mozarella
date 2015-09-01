import pyaudio
import wave
import audioop
import numpy
import pygame
import struct
import math

from services import *
from settings import Settings
		
settings = Settings()
def init():
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=1024)
    pygame.init()
    




