import pygame
import time
import math
import numpy
import threading
import waveutils
import core

from synthesis.instrument import *
from synthesis.snare import *   
from synthesis.song import Song
from synthesis.song_player import SongPlayer
from synthesis.songmaker.scale import *
from synthesis.songmaker.bank import bank
import synthesis.instruments as instruments
import synthesis.songmaker.scales as scales
 
core.init()

# --------------------------------------------------------
from random import *
song = Song(40)
inst = instruments.hardsynth
melo = instruments.melo

# drums
snare = SnareSampler()

def roi_lion():
    inst = instruments.test
    songplayer = SongPlayer()
    notes = [
        (0, 1, Note('A', 4))
    ]
    for t, hold, note in notes:
        song.add_note(t, hold, inst, note, 1.0)
    songplayer.play(song)
    songplayer.play(song)
    
def melodic_patterns():
    #roi_lion()
    #return
    inst = instruments.sinus
    songplayer = SongPlayer()
    scale = Scale(scales.blues, 'C')
    melodies = bank.melodic_patterns
    rythms = bank.rythm_patterns
    recording = []
    succession = scale.generate_arpegio(1, Note(choice(scale.notes), 4), 4, 0)
    key_id = 0
    for i in range(0, 8):
        song.clear()
        song.set_ticks(8)
        melody_rythm = choice(bank.rythms_by_category("Ternary"))
        melody = choice(bank.melodic_patterns)
        if "Ternary" in melody_rythm.categories:
            melody = choice(bank.melodic_patterns_by_category("Ternary"))
        notes_count = len(melody_rythm.holds) 
        notes = melody.generate(succession[key_id], scale, notes_count)
        t = 0
        for j in range(0, 1):
            for i in range(0, notes_count):
                duration = melody_rythm.durations[i]
                hold = melody_rythm.holds[i]
                song.add_note(t, hold, inst, notes[i], 1.0)
                print notes[i]
                t += duration
        
        key_id = (key_id+1) % len(succession)
        recording += songplayer.play(song)
    waveutils.wav_save(recording, "out/test3.wav")
    
def arpegio():
    songplayer = SongPlayer()
    blbl = ["C", "D", "E"]
    arpegios = [0, 1, 2, 3, 4]
    base_arpegio = [0, 1]
    rythms = bank.rythm_patterns
    scale_kind = scales.phrygian
    #scale = Scale(scales.algerian, 'C')#Scale(choice(scales.all_scales), choice(blbl))
    recording = []
    scale = Scale(choice(scales.all_scales), choice(blbl))
    for i in range(0, 20):
        song.clear()
        t = 0
        startnote = choice(scale.notes)
        for octave in [2, 3]:
            t1 = t
            
            notes_played = []
            rythm = choice(rythms)
            note_count = len(rythm.holds)
            for i, note in enumerate(scale.generate_arpegio(choice(arpegios), Note(startnote, octave), note_count, 0)):
                duration = rythm.durations[i]
                hold = rythm.holds[i]
                notes_played.append(note)
                song.add_note_old(t, hold, inst, note.name, note.octave+i%2, 1)
                t += duration
                
            song.add_note_old(t1, 1, snare, 'E', 0, 1)
            for i in range(0, int(rythm.get_measures_count())*4):
                pass
                #song.add_note_old(t1+i, 0.5, snare, 'E', 1, 1)
                #song.add_note_old(t1+i*4, 0.5, snare, 'C', 1, 1)
            
            # Sustain
            for i, note in enumerate(scale.generate_chord_old(0, Note(notes_played[0].name, octave-2))):
                hold = rythm.get_measures_count() * 4
                song.add_note_old(t1+0.001, hold, melo, note.name, note.octave, 0.7)

            # Wawa
            # for i, note in enumerate(scale.generate_chord(0, Note(notes_played[0].name, octave-2))):
            #     total_ticks = rythm.get_measures_count() * 4
            #     mult = 2.0
            #     for j in range(0, int(total_ticks*mult)):
            #         song.add_note_old(t1+j/mult+0.001, 1.0/mult, inst, notes_played[j%len(notes_played)].name, 1+j%2, 0.7)
            
        recording += songplayer.play(song)
    waveutils.wav_save(recording, "out/test2.wav")
    
def megacool():
    songplayer = SongPlayer()
    while True:
        song.clear()
        song.set_ticks(4)
        gamme = ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb', 'C']
        octaves = [0, 1, 2, 3, 4, 5]
        deform = [1.001, 1.002, 1.003, 1.004, 1.005, 1.01, 0.99, 0.98]
        patterns = [[1, 1, 1, 1], [1, 0.5, 0.5, 1, 1], [2, 2], [1, 0.5, 1, 0.5, 1, 1], [1, -1, 1, 1], [1, 1, -2]]
        t = 0
        for i in range(0, 4):
            song.add_note_old(i, 0.5, inst, 'C', 4, 1)
            duration = 1
            notes = [choice(gamme), choice(gamme)]
            octaves = [2, 1]
            for j in range(0, 4):
                song.add_note_old(t+j, duration, inst, notes[0], octaves[j%2], 0.754)
                pass
                
            cur = 0
            pattern = choice(patterns)
            for duration in pattern:
                if duration > 0:
                    song.add_note_old(t+cur, duration, melo, choice(gamme), 4, 1)
                cur += duration
    
            t += 4
        
        songplayer.play(song)
    #arr = song.generate()
    #waveutils.wav_save(arr, "test.wav")
    
def randosong():
    # gamme = ['C', 'Eb', 'F', 'F#', 'G', 'Bb', 'C']
    #gamme = ['D', 'E', 'F#', 'G', 'G#', 'A#', 'C', 'D']
    gamme = ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb', 'C']
    octaves = [4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1]
    intervals = [1, -1]#[1, 0, -1, 2, -2, 2, 4]
    times = [1, 1, 1, 1,
            1, 0.5, 0.5, 1, 1,
            2, 2]
    
    
    noteid = 4
    for i in range(0, 150):
        interv = choice(intervals)
        noteid = (interv + noteid + len(gamme)) % len(gamme)
        prevnoteid = (noteid - 2 + len(gamme)) % len(gamme)
        note = gamme[noteid]
        time = times[i % len(times)]
        octave = choice(octaves)
        song.add_note_old(i, time, inst, note, octave, 1)
        if i % 8 == 0 and False:
            song.add_note_old(i, 8, inst, note, 0, 0.5)
            song.add_note_old(i, 8, inst, note, 1, 0.5)
            
            song.add_note_old(i, 1, inst, note, 1, 1)
            song.add_note_old(i+2, 1, inst, note, 1, 1)
            song.add_note_old(i+4, 1, inst, note, 1, 1)
            song.add_note_old(i+6, 1, inst, gamme[prevnoteid], 1, 1)
            song.add_note_old(i+7, 1, inst, note, 1, 1)
    
    arr = song.generate()

    waveutils.wav_save(arr, "out/test.wav")

melodic_patterns()
