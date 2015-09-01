from rythm_pattern import *

fast3 = RythmPattern(["Rythm", "Fast"], [0.5 for x in range(0, 8)])
fast4 = RythmPattern(["Rythm","Fast"],[0.25 for x in range(0, 16)])
fast = RythmPattern(["Rythm","Fast"],[0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
fast2 = RythmPattern(["Fast"],[0.25, 0.25, 0.5, 0.5, 0.5, 1, 1])
simple = RythmPattern(["Rythm","Basic"], [1, 1, 1, 1])
simple2 = RythmPattern(["Basic", "Groove"],[0.5, 1, 1, 1, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5])
simple_variant = RythmPattern(["Basic", "Groove"],[1, 0.5, 0.5, 1, 1])
simple_offbeat = RythmPattern(["Basic", "Groove"], [0.5, 1, 1, 1, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5]) 
offbeat = RythmPattern(["Groove"],[0.5, 0.25, 0.25, 0.5, 1, 1, 0.5], [0.5, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5])
calm = RythmPattern(["Slow"],[2, 2])
calm2 = RythmPattern(["Slow", "Dark"],[2, 2, 4])
metal = RythmPattern(["Rythm","Metal", "Fast"], [0.5, 0.5, 1, 0.5, 0.5, 1])
metal2 = RythmPattern(["Rythm","Metal", "Fast"], [0.5, 0.5, 1, 0.5, 1, 0.5])
ternary = RythmPattern(["Rythm","Ternary", "Metal"], [1, 1, 1, 1, 1, 1, 1, 1], [0.75, 0.5, 0.5, 0.75, 0.5, 0.5, 0.75, 0.5])
all_rythms = [simple, simple2, simple_variant, simple_offbeat, 
			  offbeat, calm, calm2, fast, fast2, fast3, fast4, 
			  metal, metal2, ternary]