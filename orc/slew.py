from pippi import dsp
import time
import pygame.midi

pygame.midi.init()

def play(ctl):
    beat = dsp.mstf(dsp.rand(100, 300))
    out = dsp.pad('', 0, beat)
    m = pygame.midi.Output(2)

    #m.write([ [[0xFA], time.time()] ])
    m.write([ [[0xF8], time.time()] ])

    return out
