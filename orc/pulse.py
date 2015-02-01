# as in tambura
from pippi import dsp
from pippi import tune

midi = {'lpd': 3}

def play(ctl):
    param = ctl.get('param')
    lpd = ctl.get('midi').get('lpd')

    pw = lpd.get(7, low=0.001, high=1, default=1)
    modr = dsp.rand(0, 0.005)
    modf = dsp.rand(0.01, 0.05)
    amp = lpd.get(8, low=0, high=2, default=0)

    length = dsp.mstf(lpd.get(6, low=40, high=1000, default=100))
    divs = [1, 2, 3.0, 4]
    div = divs[lpd.geti(5, low=0, high=len(divs) - 1)]
    #div = dsp.randchoose(divs)

    length = int(length / div)

    wf = dsp.breakpoint([0] + [ dsp.rand(-1, 1) for w in range(5) ] + [0], 512)
    wf = dsp.wavetable('sine2pi', 512)
    win = dsp.wavetable('sine', 512)
    mod = dsp.breakpoint([0] + [ dsp.rand(0, 1) for m in range(5) ] + [0], 512)

    layers = []

    chord = [ dsp.randchoose([1, 3, 5, 6, 8, 16]) for c in range(dsp.randint(2, 4)) ]

    notes = tune.fromdegrees(chord, root='d', octave=dsp.randint(1, 2))

    for freq in notes:
        a = amp * dsp.rand(0.1, 0.75)

        layer = dsp.pulsar(freq, length, pw, wf, win, mod, modr, modf, a)
        layer = dsp.pan(layer, dsp.rand())

        layers += [ layer ]

    out = dsp.mix(layers)
    out = dsp.taper(out)
    out = dsp.env(out, 'phasor')

    #out = dsp.pad(out, 0, length)

    #out = out * 4

    return out
