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

def parsebeat(pattern, division, beat, length, callback):
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
    for i, (amp, length) in enumerate(beats):
        if amp < 0:
            out += callback(length, i)
        else:
            out += dsp.pad('', 0, length)

    out = [ callback(length, i=i, amp=amp) if amp > 0 else dsp.pad('', 0, length) for i, (amp, length) in enumerate(beats) ]
    out = ''.join(out)

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


