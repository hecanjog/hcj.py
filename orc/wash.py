from pippi import dsp
from pippi import tune

midi = {'pc': 3, 'lpd': 7}

def play(ctl):
    param = ctl.get('param')
    lpd = ctl.get('midi').get('lpd')

    pc = ctl.get('midi').get('pc')
    pc.setOffset(111)

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
    area = dsp.randchoose(['high', 'mid', 'pitch', 'low'])

    dsp.log(area)

    freqs = dsp.randchoose(gamut[area])

    freqscale = pc.get(13, low=0.125, high=2, default=1)
    freqscale = dsp.rand(0.125, 2)

    low = freqs[0] * freqscale
    high = freqs[1] * freqscale

    wform = dsp.randchoose(['sine2pi', 'tri', 'vary', 'square'])

    timescale = pc.get(5, low=1, high=4, default=1)
    timescale = dsp.rand(1, 4)
    lengthscale = pc.get(12, low=0.125, high=2.5)
    lengthscale = dsp.rand(0.125, 2.5)

    amp = pc.get(4, low=0, high=1, default=0.5)
    amp = dsp.rand(0, 0.5)

    if area == 'high':
        low = dsp.rand(low * 0.9, low)
        high = dsp.rand(high, high * 1.1)

        length = dsp.stf(dsp.rand(0.01, 0.3) * lengthscale)
        out = dsp.bln(length, low, high, wform)
        out = dsp.env(out, 'phasor')

        if dsp.rand() > 10.5:
            beep = dsp.tone(dsp.flen(out), high * 2, amp=dsp.rand(0.5, 1))
            out = dsp.mix([out, beep])

        out = dsp.pad(out, 0, dsp.mstf(dsp.rand(1, 400) * timescale))
        out = out * dsp.randint(1, 3)
        out = dsp.drift(out, dsp.rand(0, 1))

    elif area == 'mid':
        low = dsp.rand(low * 0.9, low)
        high = dsp.rand(high, high * 1.1)

        length = dsp.stf(dsp.rand(0.01, 0.5) * lengthscale)
        out = dsp.bln(length, low, high, wform)
        out = dsp.env(out, 'random')

        if timescale > 1:
            out = dsp.pad(out, 0, dsp.mstf(500 * timescale * dsp.rand(0.5, 1.5)))


    elif area == 'pitch':
        low = dsp.rand(low * 0.9, low)
        high = dsp.rand(high, high * 1.1)

        length = dsp.stf(dsp.rand(0.01, 0.5) * lengthscale)
        out = dsp.bln(length, low, high, wform)
        out = dsp.env(out, 'random')

        if timescale > 1:
            out = dsp.pad(out, 0, dsp.mstf(500 * timescale * dsp.rand(0.5, 1.5)))


    elif area == 'low':
        low = dsp.rand(low * 0.9, low)
        high = dsp.rand(high, high * 1.1)

        length = dsp.stf(dsp.rand(0.2, 2) * lengthscale)
        out = dsp.bln(length, low, high, wform)
        out = dsp.env(out, 'random')
        out = dsp.mix([out, dsp.tone(length, low)])

        if timescale > 1:
            out = dsp.pad(out, 0, dsp.mstf(500 * timescale * dsp.rand(0.5, 1.5)))


    if dsp.rand() > pc.get(14, low=0, high=1, default=0.75):
        plength = length * dsp.randint(2, 6)
        freq = tune.ntf(param.get('key', default='c'), octave=dsp.randint(0, 4))
        out = dsp.mix([ dsp.pine(out, plength, freq), dsp.pine(out, plength, freq * 1.25) ])
        out = dsp.fill(out, length)

    out = dsp.pan(out, dsp.rand())
    out = dsp.amp(out, amp)

    return out
