"""
Most drums follow this (named) param format:
    length
    i
    amp

'i' is meant to be an arbitrary index - probably the count of the current beat.

Every drum can be called with no params and it will return /something/ without 
complaining. It's cooler to tell them to do something though.

"""

from pippi import dsp
from pippi import tune
import fx

def parsebeat(pattern, division, beat, length, callback, swing=0):
    subbeat = (beat * 4) / division
    nbeats = length / subbeat

    pattern = [ pattern[ i % len(pattern)] for i in range(nbeats) ]

    beats = []
    elapsed = 0

    for i, glyph in enumerate(pattern):
        elapsed += subbeat

        if glyph == 'x' or glyph == '-':
            glyph_type = 1
        else:
            glyph_type = 0

        next = None
        if i < len(pattern) - 1:
            next = pattern[i + 1]

        transition = ((glyph == 'x' or glyph == '-') and (next == ' ' or next == 'x')) or (glyph == ' ' and next == 'x')

        if transition or next is None:
            beats += [ (glyph_type, elapsed) ]
            elapsed = 0

    out = ''
    for i, (amp, beat_length) in enumerate(beats):
        if amp > 0:
            if i % 2 == 1 and swing > 0:
                swing_percent = (swing / 100.0) * 0.75 # actual range is 0 - 75%
                delay_length = int(beat_length * swing_percent)
                o = callback(beat_length - delay_length, i=i, amp=amp)
                o = dsp.pad(o, delay_length, 0)
                out += o
            else:
                out += callback(beat_length, i=i, amp=amp)
        else:
            out += dsp.pad('', 0, beat_length)

    return out

def sinekick(length=22050, i=0, amp=0.5):
    if amp == 0:
        return dsp.pad('', 0, length)

    fhigh = 160.0
    flow = 60.0
    fdelta = fhigh - flow

    target = length
    pos = 0
    fpos = fhigh

    out = ''
    while pos < target:
        # Add single cycle
        # Decrease pitch by amount relative to cycle len
        cycle = dsp.cycle(fpos)
        pos += dsp.flen(cycle)
        fpos = fpos - 30.0
        out += cycle

    out = dsp.amp(out, amp)
    return dsp.env(out, 'phasor')

def kick(length=22050, i=0, amp=0.5):
    wav = dsp.breakpoint([0] + [ dsp.rand(-1,1) for w in range(20) ] + [0], 512)
    win = dsp.wavetable('sine', 512)
    mod = dsp.wavetable('phasor', 512)

    root = 30.0
    klen = length / 4
    pw = dsp.rand(0.1, 1)

    amp = dsp.rand(0.5, 1.0)

    mFreq = 1.0 / dsp.fts(klen)

    k = dsp.pulsar(root, klen, pw, wav, win, mod, 2.0, mFreq, amp)

    k = dsp.mix([ sinekick(amp=dsp.rand(0.4, 0.7), length=klen), k ])

    k = dsp.env(k, 'phasor')

    k = dsp.pad(k, 0, length - klen)

    return k

def clap(length=22050, i=0, amp=0.5, root=3000.0, pw=None):
    wav = dsp.breakpoint([0] + [ dsp.rand(-1,1) for w in range(50) ] + [0], 512)
    win = dsp.wavetable('sine', 512)
    mod = dsp.wavetable('phasor', 512)

    klen = length / dsp.randint(2, 5) 
    if pw is None:
        pw = dsp.rand(0.1, 1)

    amp = dsp.rand(0.75, 1.0)

    mFreq = 1.0 / dsp.fts(klen)

    k = dsp.pulsar(root, klen, pw, wav, win, mod, 1.0, mFreq, amp) 
    #k = orc.kick(dsp.rand(0.4, 0.7), klen)

    k = dsp.env(k, 'phasor')

    k = dsp.pad(k, 0, length - klen)

    return k

def roll(snd, length=None, numlayers=2, minlen=10, maxlen=80, env=True, bend=True):
    layers = []

    for _ in range(numlayers):
        if length is None:
            numbeats = dsp.randint(20, 50)
        else:
            numbeats = length / dsp.mstf(minlen)

        lengths = dsp.breakpoint([ dsp.rand(minlen, maxlen) for _ in range(dsp.randint(5, numbeats/2)) ], numbeats)

        layer = ''
        for l in lengths:
            layer += dsp.fill(snd, dsp.mstf(l), silence=True)

        if bend:
            layer = fx.bend(layer, [ dsp.rand(0, 1) for _ in range(dsp.randint(5, 20)) ], dsp.rand(0.02, 1))

        if env:
            layer = fx.penv(layer)

        layers += [ layer ]

    out = dsp.mix(layers)
    out = dsp.fill(out, length)

    return out
