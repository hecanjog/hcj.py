from pippi import dsp
from pippi import tune

def sinekick(amp, length):
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

def kick(length, i=0):
    wav = dsp.breakpoint([0] + [ dsp.rand(-1,1) for w in range(20) ] + [0], 512)
    win = dsp.wavetable('sine', 512)
    mod = dsp.wavetable('phasor', 512)

    root = 30.0
    klen = length / 4
    pw = dsp.rand(0.1, 1)

    amp = dsp.rand(0.5, 1.0)

    mFreq = 1.0 / dsp.fts(klen)

    k = dsp.pulsar(root, klen, pw, wav, win, mod, 2.0, mFreq, amp)

    k = dsp.mix([ sinekick(dsp.rand(0.4, 0.7), klen), k ])

    k = dsp.env(k, 'phasor')

    k = dsp.pad(k, 0, length - klen)

    return k

def clap(length, i=0):
    wav = dsp.breakpoint([0] + [ dsp.rand(-1,1) for w in range(50) ] + [0], 512)
    win = dsp.wavetable('sine', 512)
    mod = dsp.wavetable('phasor', 512)

    root = 3000.0
    klen = length / dsp.randint(2, 5) 
    pw = dsp.rand(0.1, 1)

    amp = dsp.rand(0.75, 1.0)

    mFreq = 1.0 / dsp.fts(klen)

    k = dsp.pulsar(root, klen, pw, wav, win, mod, 1.0, mFreq, amp) 
    #k = orc.kick(dsp.rand(0.4, 0.7), klen)

    k = dsp.env(k, 'phasor')

    k = dsp.pad(k, 0, length - klen)

    return k

def hat(length, i=0):
    wav = dsp.wavetable('sine2pi', 512)
    win = dsp.wavetable('sine', 512)
    mod = dsp.wavetable('phasor', 512)

    chords = [
        ['e', 'g#', 'a'],
        ['e', 'd', 'a'],
        ['c#', 'b', 'a', 'f#'],
    ]

    pw = dsp.rand(0.1, 1)

    roots = chords[i % len(chords)]
    roots = [ tune.ntf(n) for n in roots ]

    klen = length / dsp.randint(1, 4)

    amp = dsp.rand(0.3, 0.5)

    mFreq = dsp.rand(0.5, 1.0) / dsp.fts(klen)

    layers = []

    for root in roots:
        k = dsp.pulsar(root, klen, pw, wav, win, mod, 0.005, mFreq, amp) 
        k = dsp.env(k, 'sine')
        k = dsp.pan(k, dsp.rand())
        k = dsp.pad(k, 0, length - klen)

        layers += [ k ]

    out = dsp.mix(layers)

    return out


