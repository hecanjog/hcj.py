from pippi import dsp
from pippi import tune

midi = {'lpd': 3}

def play(ctl):
    param = ctl.get('param')
    lpd = ctl.get('midi').get('lpd')

    freqs = [25, 55, 109, 222, 440, 550, 660, 770, 880]
    freqs = [55, 110, 440, 220, 880]
    length = dsp.mstf(dsp.rand(100, 2000))
    length = dsp.mstf(3000)

    layers = []
    for freq in freqs:
        freq = freq * 4 + dsp.rand(0.1, 1.5)

        if freq < 100:
            amp = 0.3
        else:
            amp = 0.01

        layer = dsp.mix([ dsp.tone(length, freq, amp=amp), dsp.tone(length, freq + dsp.rand(1, 10), amp=amp) ])
        layers += [ layer ]

    out = dsp.mix(layers)

    return out
