from pippi import dsp
from pippi import tune

midi = {'lpd': 3}

def play(ctl):
    param = ctl.get('param')
    lpd = ctl.get('midi').get('lpd')

    freqs = [
        (10000, 15000),
        (5000, 15000),
        (5000, 10000),
    ]

    low = dsp.rand(50, 100) 
    high = dsp.rand(80, 120)

    low = 80
    high = 120

    wform = 'sine2pi'

    amp = lpd.get(5, low=0, high=1, default=0)

    low = dsp.rand(low * 0.9, low)
    high = dsp.rand(high, high * 1.1)

    length = dsp.mstf(lpd.get(1, low=10, high=900)) 

    if dsp.rand() > 10.5:
        length = length / 2

    pulselength = lpd.geti(2, low=dsp.mstf(10), high=length, default=length)

    out = dsp.bln(pulselength, low, high, wform)
    out = dsp.env(out, 'phasor')

    if dsp.rand() > 10.1:
        beep = dsp.tone(dsp.flen(out), dsp.rand(12000, 12000), amp=dsp.rand(0.5, 1))
        out = dsp.mix([out, beep])

    out = dsp.drift(out, dsp.rand(0, 1))
    out = dsp.pad(out, 0, length - dsp.flen(out))

    out = dsp.pan(out, dsp.rand())
    out = dsp.amp(out, amp)

    return out
