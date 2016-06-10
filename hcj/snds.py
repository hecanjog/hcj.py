from pippi import dsp, tune
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

def getMatches(inst, midi_note, wildcard=''):
    inst = inst.lower()
    path = os.path.join(snddir, 'iowa/%s/%s.%s.%s*.wav' % (inst, midi_note, inst, wildcard))
    dsp.log(path)
    files = glob.glob(path)

    if len(files) == 0 and midi_note > 120:
        raise ValueError('No matching pitch (%s) found for %s' % (midi_note, inst))
    elif len(files) == 0:
        midi_note += 12
        files = getMatches(inst, midi_note)

    return files

def iowa(inst, freq=440, wildcard=''):
    midi_note = tune.ftomi(freq)

    files = getMatches(inst, midi_note, wildcard)
    filename = dsp.randchoose(files)

    return dsp.read(filename).data

