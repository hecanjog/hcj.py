from pippi import dsp
from pippi import tune
from hcj import fx

midi = {'lpd': 3}

def play(ctl):
    param = ctl.get('param')

    lpd = ctl.get('midi').get('lpd')

    key = param.get('key', default='d')

    chords = param.get('chords', default='I.ii.vi.V').split('.')

    chord_index = param.get('chord_index', default=0)
    chord = tune.chord(chords[chord_index % len(chords)], key, octave=2)
    chord.reverse()

    reps = param.get('reps', default=4)
    rep = param.get('rep', default=0)

    freq = chord[int(rep) % len(chord)]

    if dsp.rand() > 0.5:
        freq *= 2**dsp.randint(0, 2)

    pw = lpd.get(1, low=0.1, high=1, default=1)
    length = dsp.mstf(lpd.get(2, low=50, high=1500, default=500))

    wf = dsp.wavetable('tri', 512)
    win = dsp.wavetable('sine', 512)
    mod = [ dsp.rand(0, 1) for m in range(512) ]
    modr = dsp.rand(0.01, 0.05)
    modf = dsp.rand(0.5, 2)
    amp = 0.3

    out = dsp.pulsar(freq, length, pw, wf, win, mod, modr, modf, amp)

    out = dsp.env(out, 'phasor')
    out = dsp.taper(out, dsp.mstf(10))
    out = dsp.pan(out, dsp.rand())

    param.set('rep', (rep + 1) % reps)

    return out
