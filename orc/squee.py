from pippi import dsp
from pippi import tune

midi = {
    'dpc': 5,
    'lpd': 3
}

def play(ctl):
    dpc = ctl.get('midi').get('dpc')
    lpd = ctl.get('midi').get('lpd')

    print lpd.get(1)

    dpc.setOffset(111)
    pw = dpc.get(1, low=0.01, high=1)

    scale = [1, 2, 3, 6, 9]
    scale = [1, 4, 6, 8]
    scale = [1, 3, 5, 9]
    scale = tune.fromdegrees(scale, octave = dpc.geti(4, low=0, high=4))

    freq = dsp.randchoose(scale)

    length = dsp.stf(dpc.get(2, low=0.1, high=8) * dsp.rand(0.5, 1.5))
    wf = dsp.wavetable('sine2pi')
    win = dsp.wavetable('sine')
    mod = [ dsp.rand(0, 1) for m in range(1000) ]
    modr = dpc.get(5, low=0, high=0.3)
    modf = dpc.get(6, low=0.001, high=10)
    amp = dpc.get(3, low=0, high=1)

    out = dsp.pulsar(freq, length, pw, wf, win, mod, modr, modf, amp)

    out = dsp.env(out, dsp.randchoose(['sine', 'tri']))
    out = dsp.pan(out, dsp.rand())

    return out
