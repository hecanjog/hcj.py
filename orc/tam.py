# as in tambura
from pippi import dsp
from pippi import tune

midi = {'lpd': 3}

def play(ctl):
    param = ctl.get('param')
    lpd = ctl.get('midi').get('lpd')

    freqs = tune.fromdegrees([1, 3, 5, 6, 9], octave=1)
    freq = dsp.randchoose(freqs)

    pw = lpd.get(5, low=0.001, high=1, default=1)
    modr = dsp.rand(0.01, 0.05)
    modf = dsp.rand(2, 20)
    amp = lpd.get(8, low=0, high=2, default=0)

    length = dsp.stf(dsp.rand(8, 10))

    wf = dsp.breakpoint([0] + [ dsp.rand(-1, 1) for w in range(5) ] + [0], 512)
    win = dsp.wavetable('sine', 512)
    mod = [ dsp.rand(0, 1) for m in range(1024) ]

    layers = []

    for i in range(dsp.randint(2, 8)):
        f = freq * (i + 1)
        a = amp * dsp.rand(0.1, 1)
        layer = dsp.pulsar(f, length, pw, wf, win, mod, modr, modf, a)
        layer = dsp.env(layer, dsp.randchoose(['sine', 'tri', 'line', 'phasor']))
        layer = dsp.taper(layer)
        layer = dsp.pan(layer, dsp.rand())
        layers += [ layer ]

    out = dsp.mix(layers)
    out = dsp.env(out, 'sine')
    out = dsp.env(out, 'hann')
    out = dsp.taper(out)

    return out
