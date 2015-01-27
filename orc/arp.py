from pippi import dsp
from pippi import tune

def play(ctl):
    param = ctl.get('param')

    key = param.get('key', default='d')

    chords = param.get('chords', default='I ii7 v vi').split(' ')

    chord = param.get('chord', default=chords[0])
    chord = tune.chord(chord, key, octave=2)
    chord.reverse()

    reps = param.get('reps', default=4)
    rep = param.get('rep', default=0)

    freq = chord[int(rep) % len(chord)]

    if dsp.rand() > 0.5:
        freq *= 2**dsp.randint(0, 2)

    length = dsp.stf(0.1)
    pw = dsp.rand(0.7, 1)
    wf = dsp.wavetable('sine2pi', 512)
    win = dsp.wavetable('sine', 512)
    mod = [ dsp.rand(0, 1) for m in range(512) ]
    modr = dsp.rand(0.001, 0.02)
    modf = dsp.rand(0.5, 2)
    amp = 0.3

    out = dsp.pulsar(freq, length, pw, wf, win, mod, modr, modf, amp)

    out = dsp.adsr(out, a=10, s=0.1, d=50, r=200)
    out = dsp.pan(out, dsp.rand())

    param.set('rep', (rep + 1) % reps)

    return out
