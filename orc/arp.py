from pippi import dsp
from pippi import tune
from hcj import fx

midi = {'pc': 3}

def play(ctl):
    param = ctl.get('param')

    lpd = ctl.get('midi').get('pc')
    lpd.setOffset(111)


    key = 'g'

    #bd = dsp.read('/home/hecanjog/sounds/drums/Tinyrim2.wav').data
    #bd = dsp.read('/home/hecanjog/sounds/drums/Jngletam.wav').data
    #bd = dsp.read('/home/hecanjog/sounds/drums/78oh.wav').data
    #bd = dsp.amp(bd, 1)
    #bd = dsp.transpose(bd, dsp.rand(0.65, 0.72) / 1)
    #bd = dsp.transpose(bd, dsp.rand(0.3, 0.32) / 1)

    chord = tune.fromdegrees([1,8], root='g', octave=dsp.randint(0,2))
    chord.reverse()
    chord = dsp.rotate(chord, lpd.geti(4, low=0, high=len(chord)-1))
    #chord = dsp.randshuffle(chord)

    reps = param.get('reps', default=16)
    rep = param.get('rep', default=0)
    beat = dsp.bpm2frames(130) / 4
    beat = dsp.mstf(4100) / 32
    #length = beat

    out = ''
    for n in range(4):
        freq = chord[int(rep) % len(chord)]

        if dsp.rand() > 0.5:
            freq *= 2**dsp.randint(0, lpd.geti(7, low=0, high=8, default=0))

        pw = lpd.get(8, low=0.1, high=1, default=1)
        #length = dsp.mstf(lpd.get(2, low=50, high=2500, default=500) * dsp.rand(0.5, 2))
        length = dsp.mstf(lpd.get(14, low=50, high=5000, default=500))

        wf = dsp.wavetable('tri', 512)
        wf = dsp.wavetable('impulse', 512)
        wf = dsp.wavetable('sine2pi', 512)
        wf = dsp.breakpoint([0] + [ dsp.rand(-1,1) for w in range(lpd.geti(15, low=4, high=200, default=4)) ] + [0], 512)

        win = dsp.wavetable('sine', 512)
        mod = [ dsp.rand(0, 1) for m in range(512) ]

        modr = dsp.rand(0.01, 0.02)
        modr = lpd.get(16, low=0.01, high=1, default=1)

        modf = dsp.rand(0.5, 2)

        amp = lpd.get(6, low=0, high=2, default=0)
        amp = dsp.rand(0, 2)

        o = dsp.pulsar(freq, length, pw, wf, win, mod, modr, modf, amp)
        o = dsp.env(o, 'random')
        o = dsp.taper(o, dsp.mstf(10))
        o = dsp.pan(o, dsp.rand())

        rep = rep + 1

        out += o

    #out = dsp.mix([ dsp.fill(bd, dsp.flen(out), silence=True), out ])

    param.set('rep', (rep + 1) % reps)

    return out
