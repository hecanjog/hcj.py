import subprocess
from pippi import dsp
import os

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

    cmd = ' '.join(cmd) + ' /tmp/infile%s.wav /tmp/outfile%s.wav' % (pid, pid)

    dsp.write(snd, '/tmp/infile%s' % pid, cwd=False)

    with open(os.devnull, 'w') as devnull:
        p = subprocess.Popen(cmd, stdout=devnull, stderr=devnull, shell=True)
        p.wait()

    out = dsp.read('/tmp/outfile%s.wav' % pid).data

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


