from pippi import dsp
from pippi import tune

def kick(length, i=0):
    root = 30.0
    klen = length / 4
    pw = dsp.rand(0.1, 1)

    amp = dsp.rand(0.5, 1.0)

    mFreq = 1.0 / dsp.fts(klen)

    k = dsp.pulsar(root, klen, pw, wav, win, mod, 2.0, mFreq, amp)

    k = dsp.mix([ orc.kick(dsp.rand(0.4, 0.7), klen), k ])

    k = dsp.env(k, 'phasor')

    k = dsp.pad(k, 0, length - klen)

    return k

def clap(length, i=0):
    root = 3000.0
    klen = length / dsp.randint(2, 5) 
    pw = dsp.rand(0.1, 1)

    wav = dsp.breakpoint([0] + [ dsp.rand(-1,1) for w in range(50) ] + [0], 512)
    amp = dsp.rand(0.75, 1.0)

    mFreq = 1.0 / dsp.fts(klen)

    k = dsp.pulsar(root, klen, pw, wav, win, mod, 1.0, mFreq, amp) 
    #k = orc.kick(dsp.rand(0.4, 0.7), klen)

    k = dsp.env(k, 'phasor')

    k = dsp.pad(k, 0, length - klen)

    return k

def hat(length, i=0):
    chords = [
        ['e', 'g#', 'a'],
        ['e', 'd', 'a'],
        ['c#', 'b', 'a', 'f#'],
    ]

    pw = dsp.rand(0.1, 1)

    roots = chords[i % len(chords)]
    roots = [ tune.ntf(n) for n in roots ]

    klen = length / dsp.randint(1, 4)

    wav = dsp.wavetable('sine2pi', 512)
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


