# as in tambura
from pippi import dsp
from pippi import tune

midi = {'lpd': 3}

def play(ctl):
    param = ctl.get('param')
    lpd = ctl.get('midi').get('lpd')

    scale = [ dsp.randchoose([1, 3, 5, 8]) for s in range(dsp.randint(2, 4)) ]

    freqs = tune.fromdegrees(scale, root='e', octave=dsp.randint(1, 3))
    freq = dsp.randchoose(freqs)

    pw = lpd.get(5, low=0.001, high=1, default=1)
    modr = dsp.rand(0, 0.005)
    modf = dsp.rand(0.01, 0.05)
    amp = lpd.get(7, low=0, high=2, default=0)

    length = dsp.stf(dsp.rand(8, 10))
    length = dsp.stf(lpd.get(2, low=8, high=14, default=1) * dsp.rand(0.75, 2))

    wf = dsp.breakpoint([0] + [ dsp.rand(-1, 1) for w in range(5) ] + [0], 512)
    wf = dsp.wavetable('sine2pi', 512)
    #wf = dsp.wavetable('sine2pi', 512)
    win = dsp.wavetable('sine', 512)
    mod = dsp.breakpoint([0] + [ dsp.rand(0, 1) for m in range(5) ] + [0], 512)

    layers = []

    harmonics = [1]

    for harmonic in harmonics:
        f = freq * harmonic
        if harmonic > 4:
            a = dsp.rand(0.001, 0.05)
        else:
            a = amp * dsp.rand(0.05, 0.2)

        layer = dsp.pulsar(f, length, pw, wf, win, mod, modr, modf, a)
        layer = dsp.env(layer, dsp.randchoose(['sine', 'tri', 'line', 'phasor']))
        layer = dsp.taper(layer)
        layer = dsp.pan(layer, dsp.rand())
        layer = dsp.mix([ dsp.drift(layer, dsp.rand(0.01, 0.03)), layer ])

        if dsp.rand() > 10.5:
            layer = dsp.vsplit(layer, dsp.mstf(50), dsp.mstf(500))
            bit = dsp.randchoose(layer)
            bit = bit * dsp.randint(1, 3)
            bit = dsp.transpose(bit, dsp.randchoose([1, 2, 4, 8]))
            layer = ''.join(layer)
            layer = dsp.insert_into(layer, bit, dsp.randint(0, dsp.flen(layer) - dsp.flen(bit)))

        layers += [ layer ]

    out = dsp.mix(layers)
    out = dsp.env(out, 'sine')
    out = dsp.env(out, 'hann')
    out = dsp.taper(out)

    return out
