from pippi import dsp

def play(ctl):
    param = ctl.get('param')

    idxWf = param.get('idxWf', default=0)
    idxWin = param.get('idxWin', default=0)
    idxMod = param.get('idxMod', default=0)
    
    freq = 220
    length = 4410
    pw = dsp.rand()
    wf = dsp.wavetable('sine2pi', 512)
    win = dsp.wavetable('sine', 512)
    mod = dsp.wavetable('sine', 512)
    modr = 0
    modf = 1
    amp = 0.3

    idxWf, idxWin, idxMod, out = dsp.pulsarstream(freq, length, pw, wf, win, mod, modr, modf, amp, idxWf, idxWin, idxMod)

    #out = dsp.taper(out, dsp.htf(freq))

    param.set('idxWf', idxWf)
    param.set('idxWin', idxWin)
    param.set('idxMod', idxMod)

    return out
