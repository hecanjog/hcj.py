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

def spider(snd, numlayers=10, numgrains=20, minlen=40, lenranges=(300,500)):
    layers = []

    for layer in range(numlayers):
        lenrange = dsp.rand(lenranges[0], lenranges[1])
        lengths = dsp.wavetable('hann', numgrains * 2)[:numgrains]
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

        layers += [ dsp.env(grains, 'phasor') ]

    return dsp.mix(layers)


