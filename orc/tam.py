# as in tambura
from pippi import dsp
from pippi import tune

midi = {'lpd': 7}

def play(ctl):
    param = ctl.get('param')
    lpd = ctl.get('midi').get('lpd')

    scale = [ dsp.randchoose([1, 5, 8]) for s in range(dsp.randint(2, 4)) ]

    freqs = tune.fromdegrees(scale, root='eb', octave=dsp.randint(0, 2))
    freq = dsp.randchoose(freqs)

    pw = lpd.get(2, low=0.01, high=1, default=1)
    pw = dsp.rand(0.01, 1)
    modr = lpd.get(6, low=0.001, high=0.1)
    modr = dsp.rand(0.001, 0.005)
    modr = dsp.rand(0, modr)
    modf = dsp.rand(0.01, 0.05)
    amp = lpd.get(1, low=0, high=2, default=0)
    amp = dsp.rand(0.5, 0.8)

    length = dsp.stf(lpd.get(5, low=0.5, high=14, default=1) * dsp.rand(0.75, 2))
    length = dsp.stf(dsp.rand(1, 3) * dsp.rand(0.75, 2))

    wf = dsp.breakpoint([0] + [ dsp.rand(-1, 1) for w in range(5) ] + [0], 512)
    #wf = dsp.wavetable('sine2pi', 512)
    #wf = dsp.wavetable('sine2pi', 512)
    #win = dsp.wavetable('sine', 512)
    win = dsp.breakpoint([0] + [ dsp.rand(0, 1) for w in range(5) ] + [0], 512)
    mod = dsp.breakpoint([0] + [ dsp.rand(0, 1) for m in range(5) ] + [0], 512)

    layers = []

    harmonics = [1, 2, 3]

    for harmonic in harmonics:
        f = freq * harmonic
        if harmonic > 4:
            a = dsp.rand(0.5, 1)
        else:
            a = amp * dsp.rand(0.5, 1)

        layer = dsp.pulsar(f, length, pw, wf, win, mod, modr, modf, a * 2)
        layer = dsp.env(layer, dsp.randchoose(['sine', 'tri', 'line', 'phasor']))
        layer = dsp.taper(layer)
        layer = dsp.pan(layer, dsp.rand())
        layer = dsp.mix([ dsp.drift(layer, dsp.rand(0.01, 0.03)), layer ])

        layer = dsp.vsplit(layer, dsp.mstf(5), dsp.mstf(1500))
        layer = dsp.randshuffle(layer)
        layer = ''.join(layer)

        """
        if dsp.rand() > 0.5:
            layer = dsp.vsplit(layer, dsp.mstf(50), dsp.mstf(500))
            bit = dsp.randchoose(layer)
            bit = bit * dsp.randint(1, 3)
            bit = dsp.transpose(bit, dsp.randchoose([1, 2, 4, 8]))
            layer = ''.join(layer)
            layer = dsp.insert_into(layer, bit, dsp.randint(0, dsp.flen(layer) - dsp.flen(bit)))
        """

        layers += [ layer ]

    out = dsp.mix(layers)
    out = dsp.env(out, 'sine')
    out = dsp.env(out, 'hann')
    out = dsp.taper(out)
    #out = dsp.env(out, 'random')

    return out
