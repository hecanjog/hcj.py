from pippi import dsp
from pippi import tune

midi = {'lpd': 3}

def play(ctl):
    param = ctl.get('param')
    lpd = ctl.get('midi').get('lpd')

    gamut = {
        'high': [
            (10000, 15000),
            (5000, 15000),
            (5000, 10000),
        ],

        'mid': [
            (1000, 5000),
            (1000, 2000),
        ],

        'pitch': [
            tuple([ dsp.rand(500, 2000) for p in range(2) ]),
            tuple([ dsp.rand(100, 1000) for p in range(2) ]),
            tuple([ dsp.rand(1000, 5000) for p in range(2) ]),
        ],

        'low': [
            (20, 5000),
            (30, 10000),
            (40, 10000),
        ]
    }

    area = param.get('wash-area', default='high')

    dsp.log(area)

    freqs = dsp.randchoose(gamut[area])

    low = lpd.get(1, low=10, high=5000)
    high = lpd.get(2, low=200, high=15000)

    low = freqs[0]
    high = freqs[1]

    wform = 'sine2pi'

    amp = lpd.get(3)

    if area == 'high':
        low = dsp.rand(low * 0.9, low)
        high = dsp.rand(high, high * 1.1)

        length = dsp.stf(dsp.rand(0.01, 0.3))
        out = dsp.bln(length, low, high, wform)
        out = dsp.env(out, 'phasor')
        out = dsp.pad(out, 0, dsp.mstf(dsp.rand(1, 200)))
        out = out * dsp.randint(1, 8)
        out = dsp.drift(out, dsp.rand(0, 1))

    elif area == 'mid':
        low = dsp.rand(low * 0.9, low)
        high = dsp.rand(high, high * 1.1)

        length = dsp.stf(dsp.rand(0.01, 0.5))
        out = dsp.bln(length, low, high, wform)
        out = dsp.env(out, 'random')

    elif area == 'pitch':
        low = dsp.rand(low * 0.9, low)
        high = dsp.rand(high, high * 1.1)

        length = dsp.stf(dsp.rand(0.01, 0.5))
        out = dsp.bln(length, low, high, wform)
        out = dsp.env(out, 'random')

    elif area == 'low':
        low = dsp.rand(low * 0.9, low)
        high = dsp.rand(high, high * 1.1)

        length = dsp.stf(dsp.rand(0.2, 2))
        out = dsp.bln(length, low, high, wform)
        out = dsp.env(out, 'random')
        out = dsp.mix([out, dsp.tone(length, low)])

    if dsp.rand() > 0.5:
        length = length * 4
        freq = low * 2
        out = dsp.pine(out, length, freq)

    out = dsp.pan(out, dsp.rand())
    out = dsp.amp(out, amp)

    return out
