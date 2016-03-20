from pippi import dsp
import os
import glob

snddir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'snds')

def path(snd):
    """ Return the full path to a sound given the relative path """
    return os.path.join(snddir, snd)

def load(snd):
    """ Return a sound string given a relative path to a sound """
    return dsp.read(path(snd)).data

def search(pattern):
    files = glob.glob(path(pattern))
    return [ load(snd) for snd in files ]

def iowa(inst, pitch=None):
    if pitch is None:
        pitch = 'c4'

    pitch = pitch[0].upper() + pitch[1:]

    path = os.path.join(snddir, 'iowa/%s/*%s*.wav' % (inst, pitch))
    dsp.log(path)

    files = glob.glob(path)

    if len(files) == 0:
        raise ValueError('No matching pitch (%s) found for %s' % (pitch, inst))

    filename = dsp.randchoose(files)

    return dsp.read(filename).data

