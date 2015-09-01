import pygame
import core
import threading
from services.audiostreamservice import AudioStreamService
from services.graphicsservice import GraphicsService
from services.processingservice import ProcessingService
from random import choice
from synthesis.instrument import *
from synthesis.snare import *   
from synthesis.song import Song
from synthesis.song_player import SongPlayer
from synthesis.instruments import hardsynth, melo

core.init()

FPS = 40
CHUNK = 44100/FPS
WAVE_OUTPUT_FILENAME = "out/file.wav"
gamme = ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb', 'C']
preload_octaves = [1, 2, 3, 4]
octaves = [3, 4]
deform = [1.001, 1.002, 1.003, 1.004, 1.005, 1.01, 0.99, 0.98]
intervals = [1, -1, 2, 0, 1, 1, 1, -2, -1]
patterns = [
     [1, 1, 1, 1],
    #  [1, 0.5, 0.5, 1, 1],
    #  [2, 2], 
    #  [1, 0.5, 1, 0.5, 1, 1],
    #  [1, -1, 1, 1],
    #  [1, 1, -2]]
]
hardsynth.preload(gamme, preload_octaves)
melo.preload(gamme, preload_octaves)
    
clock = pygame.time.Clock()
audio_srv = AudioStreamService(chunk_size=CHUNK)
graphics_srv = GraphicsService()
proc_srv = ProcessingService()

songplayer = SongPlayer()
song = Song(60)
done = False

def play_sound(bpm):
    # --- Generates song chunk
    song = Song(max(bpm-10, 60))
    song.clear()
    song.set_ticks(4)

    t = 0
    state = [0, 0]
    def select_note():
        interv = choice(intervals)
        state[0] = (interv + state[0] + len(gamme)) % len(gamme)
        state[1] = (state[0] - 2 + len(gamme)) % len(gamme)
        note = gamme[state[0]]
        return note
        
    for i in range(0, 8):      
        #song.add_note_old(t, 0.5, hardsynth, 'C', 1, 0.4)
        
        cur = 0
        pattern = choice(patterns)
        notes = []
        for duration in pattern:
            if duration > 0:
                note = select_note()
                notes.append(note)
                song.add_note_old(t+cur, duration, melo, select_note(), choice(octaves), 0.12)
            cur += duration
        
        duration = 1
        for j in range(0, 4):
            song.add_note_old(t+j, duration, hardsynth, notes[0], 2, 0.25)
            
        t += 4
    # Plays it
    songplayer.play_override(song)
    
# -------- Main Program Loop -----------
beatid = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            done = True
    chunk = audio_srv.read_processed_chunk()
    data = proc_srv.process(chunk, 1.0/FPS)
    graphics_srv.refresh(data)
    
    if data[3]:
        beatid = (beatid + 1)%4

    if data[3] and beatid == 1:
        print "BEAT"
        def do():
            play_sound(proc_srv.bpm)
        t = threading.Thread(target=do)
        t.start()
        
    clock.tick(FPS)
    

    
# audio_srv.save(WAVE_OUTPUT_FILENAME)
# audio_srv.dispose()