import math
def triangle(t):
    # Periode : 2*pi
    pi = math.pi * 2
    return 2 * abs(2*(t/pi - math.floor(t/pi + 0.5))) - 1