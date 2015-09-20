from pippi import dsp
from pippi import tune

midi = {'lpd': 3}

def play(ctl):
    lpd = ctl.get('midi').get('lpd')

    def rain(snd, freqs):
        layers = []

        for freq in freqs:
            #layer = dsp.pine(snd, dsp.flen(snd) * 16, freq)

            layer = dsp.pan(snd, dsp.rand())
            layer = dsp.amp(layer, 0.5)
            layer = dsp.alias(layer)
            layers += [ layer ]

        return dsp.mix(layers)

    wf = dsp.breakpoint([0] + [ dsp.rand(-1,1) for w in range(lpd.geti(7, low=4, high=200, default=0)) ] + [0], 512)
    win = dsp.wavetable('sine', 512)
    mod = [ dsp.rand(0, 1) for m in range(512) ]

    modr = lpd.get(5, low=0.01, high=1, default=1)
    modf = dsp.rand(0.5, 2)

    amp = lpd.get(3, low=0, high=0.5, default=0)

    length = dsp.mstf(lpd.get(2, low=150, high=500))
    pw = lpd.get(1, low=0.1, high=1, default=1)

    freqs = tune.fromdegrees([1,3,5], octave=2, root='c')

    freq = dsp.randchoose(freqs) / 4.0

    #o = dsp.pulsar(freq, length, pw, wf, win, mod, modr, modf, amp)
    #o = dsp.read('/home/hecanjog/sounds/guitarpluck.wav').data
    o = dsp.read('sounds/rhodes.wav').data
    o = dsp.transpose(o, dsp.randchoose([0.5, 1, 2, 1.5, 3]))
    o = dsp.fill(o, dsp.stf(dsp.rand(0.1, 2)))

    out = rain(o, freqs)

    #out = dsp.env(out, 'random')

    return out
