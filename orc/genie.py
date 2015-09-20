from hcj import snds
from pippi import dsp, tune

def play(ctl):
    pianos = ['sawvib', 'piano', 'pianooct1', 'harp', 'saw']
    pianos = ['sawvib', 'piano']
    piano = snds.load('genie/%s.wav' % dsp.randchoose(pianos))
    notes = [1,3,5]
    chord = tune.fromdegrees([ dsp.randchoose(notes) + (dsp.randchoose([0, 1]) * 8) for _ in range(dsp.randint(1, 3)) ], octave=0)
    length = dsp.stf(dsp.rand(1, 4))

    layers = []

    for freq in chord:
        p = dsp.transpose(piano, freq / 220.0)
        p = dsp.amp(p, 0.35)
        #p = dsp.pan(p, dsp.rand())
        p = dsp.fill(p, length)

        if dsp.rand() > 0.25:
            p = dsp.vsplit(p, dsp.mstf(100), dsp.mstf(500))
            p = [ dsp.pan(pp, dsp.rand()) for pp in p ]
            p = [ dsp.amp(pp, dsp.rand(0,2)) for pp in p ]
            p = [ dsp.transpose(pp, dsp.randchoose([1,2,4,8])) for pp in p ]
            p = [ dsp.taper(pp, 20) for pp in p ]
            p = [ dsp.pad(pp, 0, dsp.mstf(dsp.rand(0, 100))) for pp in p ]
            p = dsp.randshuffle(p)
            p = ''.join(p)

        if dsp.rand() > 0.75:
            p = dsp.alias(p)

        #p = dsp.env(p, 'phasor')

        layers += [ p ]

    out = dsp.mix(layers)

    return out
