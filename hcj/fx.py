import subprocess
from pippi import dsp
import os
import random

def rb(snd, length=None, speed=None, hz=None, interval=None, ratios=None, crisp=0, formant=False):
    pid = os.getpid()
    cmd = ['rubberband']

    # Time stretching
    if length is not None and dsp.flen(snd) != length and length > 0:
        cmd += [ '--duration %s' % dsp.fts(length) ] 

    # crisp setting
    cmd += [ '--crisp %s' % dsp.cap(crisp, 6, 0) ]

    # preserve formants
    if formant:
        cmd += [ '--formant' ]

    # pitch shift by speed
    if speed is not None:
        cmd += [ '--frequency %s' % speed ]

    # pitch shift by semitones
    if interval is not None:
        # TODO use pippi.tune ratios and calc frequency args
        cmd += [ '--pitch %s' % interval ]

    vpid = pid + random.randint(1, 10000)

    cmd = ' '.join(cmd) + ' /tmp/infile%s.wav /tmp/outfile%s.wav' % (vpid, vpid)

    dsp.write(snd, '/tmp/infile%s' % vpid, cwd=False)

    with open(os.devnull, 'w') as devnull:
        p = subprocess.Popen(cmd, stdout=devnull, stderr=devnull, shell=True)
        p.wait()

    out = dsp.read('/tmp/outfile%s.wav' % vpid).data
    os.remove('/tmp/outfile%s.wav' % vpid)
    os.remove('/tmp/infile%s.wav' % vpid)

    return out

def renv(snd, low=4, high=20, taper=True):
    e = [ dsp.rand() for _ in range(dsp.randint(low, high)) ]
    if taper:
        e = [0] + e + [0]

    return dsp.taper(dsp.benv(snd, e), 40)

def penv(snd, low=4, high=20):
    packets = dsp.split(snd, dsp.dsp_grain)

    ptable = dsp.breakpoint([ dsp.rand() for _ in range(dsp.randint(low, high)) ], len(packets))
    etable = dsp.breakpoint([0] + [ dsp.rand() for _ in range(dsp.randint(low, high)) ] + [0], len(packets))

    packets = [ dsp.pan(p, ptable[i], etable[i]) for i, p in enumerate(packets) ]

    return ''.join(packets)


def spider(snd, numlayers=10, numgrains=20, minlen=40, lenranges=(300,500), reverse=False, env='hann'):
    layers = []

    for layer in range(numlayers):
        lenrange = dsp.rand(lenranges[0], lenranges[1])

        if reverse:
            lengths = dsp.wavetable(env, numgrains * 2)[numgrains:]
        else:
            lengths = dsp.wavetable(env, numgrains * 2)[:numgrains]

        lengths = [ dsp.mstf(l * lenrange + minlen) for l in lengths ]
        pans = dsp.breakpoint([ dsp.rand() for p in range(numgrains / 3)], numgrains)

        startpoint = dsp.randint(0, dsp.flen(snd) - max(lengths))
    
        grains = ''

        for l, p in zip(lengths, pans):
            grain = dsp.cut(snd, startpoint, l)
            grain = dsp.env(grain, 'phasor')
            grain = dsp.taper(grain, dsp.mstf(10))
            grain = dsp.pan(grain, p)
            
            grains += grain

        if reverse:
            layers += [ dsp.env(grains, 'line') ]
        else:
            layers += [ dsp.env(grains, 'phasor') ]

    return dsp.mix(layers)

def wild(snd, factor=1):
    snd = dsp.vsplit(snd, 41, 441)
    #snd = [ dsp.fnoise(l, dsp.rand(0, factor * 0.05)) for l in snd ]
    snd = [ dsp.amp(dsp.amp(l, dsp.rand(10, factor * 30 + 20)), 0.5) for l in snd ]
    snd = ''.join(snd)

    return snd

def bend(snd, freqs=None, amount=0.02):
    out = dsp.split(snd, 441)

    if freqs is None:
        freqs = dsp.wavetable('sine', len(out))
    else:
        freqs = dsp.breakpoint(freqs, len(out))

    freqs = [ freq * amount + (1 - (amount * 0.5)) for freq in freqs ]

    out = [ dsp.transpose(grain, freq) for grain, freq in zip(out, freqs) ]

    return ''.join(out)

def glitchStutter(snd):
    """ Basically a random gate """
    snd = dsp.vsplit(snd, dsp.mstf(1, 50), dsp.mstf(50, 200))

    for i, s in enumerate(snd):
        if dsp.rand() > dsp.rand(0.5, 0.9):
            s = dsp.amp(s, dsp.rand(0, 0.15))
            s = dsp.taper(s, 20)
            snd[i] = s
        else:
            s = dsp.amp(s, dsp.rand(0.85, 1))
            snd[i] = dsp.taper(s, 20)

    snd = ''.join(snd)

    return snd

def glitchPulse(snd):
    """ 2 to 3 overlapping streams of enveloped grains at regular but phasing intervals. """

    numlayers = dsp.randint(2,3)

    layers = []
    for _ in range(numlayers):
        grains = dsp.split(snd, dsp.mstf(1, 100))
        grains = [ dsp.taper(g, 50) for g in grains ]
        grains = ''.join(grains)
        grains = penv(grains)

        layers += [ grains ]

    return dsp.mix(layers)

def glitchDetune(snd):
    """ 2 to 3 overlapping streams of enveloped grains at regular but phasing intervals. """

    numlayers = dsp.randint(2,3)

    layers = []
    for _ in range(numlayers):
        grains = dsp.split(snd, dsp.mstf(1, 100))
        grains = [ dsp.taper(g, 50) for g in grains ]
        grains = ''.join(grains)
        grains = penv(grains)
        grains = bend(grains, [ dsp.rand() for _ in range(dsp.randint(4, 10)) ], dsp.rand(0.001, 0.1))

        layers += [ grains ]

    return dsp.mix(layers)


def glitch(snd, types=None):
    if types is None:
        types = 'rand'
    
    if isinstance(types, basestring):
        types = types.split(' ')

    assert isinstance(types, list)

    for proctype in types:
        if proctype == 'stutter':
            snd = glitchStutter(snd)

        if proctype == 'pulse':
            snd = glitchPulse(snd)

        if proctype == 'rand':
            pass

        if proctype == 'rainbow':
            pass

        if proctype == 'split':
            pass

        if proctype == 'smear':
            pass

        if proctype == 'detune':
            snd = glitchDetune(snd)

        if proctype == 'destroy':
            pass

        if proctype == 'gliss':
            pass

        if proctype == 'ring':
            pass

    return snd




