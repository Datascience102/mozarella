from instrument import *
# ----------- hardsynth -----------
spectrum = []
for i, multiplier in enumerate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]):
    for offset in [0, 0.013, 0.028, -0.019, 0.026, 0.1, -0.15, 0.14, -0.12]:
        spectrum.append((multiplier, 1.0-i*0.095, offset))

hardsynth = MultipleOscillator(spectrum)

# ----------- melo -----------
spec2 = []
for i, multiplier in enumerate([1]):
    offsets = [0.10 * x for x in range(-4, 4)]
    for offset in offsets:
        spec2.append((multiplier, 1.0/max(1, (1+multiplier*5+offset*10)), offset))
melo = MultipleOscillator(spec2)

# ----------- sinus ----------
sinus = MultipleOscillator([(1, 1, 0), (2, 0.125, 0.05), (3, 0.125, 0.025)])
sinus = ADSREnvelope(sinus, 0.10, 0.2, 0.8, 1, 1, 0.4)

# test
import random
spec3 = []
multiplier = 1
for i in range(0, 1000):
    offset = random.random()
    multiplier = random.randint(1, 32)
    volume = random.random()
    spec3.append((multiplier, volume, offset))

test = MultipleOscillator(spec3)
test = ADSREnvelope(hardsynth, 0.05, 0.5, 0.8, 1, 1, 0.4)
test = Delay(test, 441)