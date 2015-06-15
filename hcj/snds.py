from pippi import dsp
import os

snddir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'snds')

def load(snd):
    path = os.path.join(snddir, snd)
    return dsp.read(path).data
