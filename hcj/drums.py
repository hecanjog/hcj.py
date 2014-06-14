"""
Most drums follow this (named) param format:
    length
    i
    bar
    amp

'i' is meant to be an arbitrary index - probably the count of the current beat.
'bar' is used as a modulo on 'i', to facilitate pattern creation and junk.

Every drum can be called with no params and it will return /something/ without 
complaining. It's cooler to tell them to do something though.

"""

from pippi import dsp
from pippi import tune

def parsebeat(pattern, beat, length, callback=None):
    b = (beat * 4) / pattern[0]
    nbeats = length / b
    p = [ pattern[1][ i % len(pattern[1])] for i in range(nbeats) ]

    beats = []
    current = 0
    for i, n in enumerate(p):
        current += b

        if n == 'x' or n == '-':
            btype = 1
        else:
            btype = 0

        next = None
        if i < len(p) - 1:
            next = p[i + 1]

        transition = ((n == 'x' or n == '-') and (next == ' ' or next == 'x')) or (n == ' ' and next == 'x')

        if transition or next is None:
            beats += [ (btype, current) ]
            current = 0

    out = ''
    for i, b in enumerate(beats):
        if b[0] == 1:
            out += callback(i, b[1])
        else:
            out += dsp.pad('', 0, b[1])

    return out


def sinekick(length=22050, i=0, bar=5, amp=0.5):
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

def kick(length=22050, i=0, bar=5, amp=0.5):
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

def clap(length=22050, i=0, bar=5, amp=0.5, root=3000.0, pw=None):
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


