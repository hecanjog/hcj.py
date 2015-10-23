from pippi import dsp
import os

snddir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'snds')

def path(snd):
    """ Return the full path to a sound given the relative path """
    return os.path.join(snddir, snd)

def load(snd):
    """ Return a sound string given a relative path to a sound """
    return dsp.read(path(snd)).data
