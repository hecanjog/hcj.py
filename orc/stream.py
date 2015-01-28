from pippi import dsp

midi = {'lpd': 3}

def play(ctl):
    param = ctl.get('param')
    lpd = ctl.get('midi').get('lpd')

    idxWf = param.get('idxWf', default=0)
    idxWin = param.get('idxWin', default=0)
    idxMod = param.get('idxMod', default=0)
    
    freq = 220
    length = dsp.mstf(lpd.get(8, low=50, high=1000, default=100))
    pw = lpd.get(5, low=0.001, high=1, default=1)
    wf = dsp.wavetable('sine2pi', 512)
    win = dsp.wavetable('sine', 512)
    mod = dsp.wavetable('sine', 512)
    #mod = dsp.breakpoint([ dsp.rand(0, 1) for m in range(10) ], 512)
    #mod = dsp.wavetable('sine', 512)
    modr = lpd.get(6, low=0, high=1, default=0)
    modf = lpd.get(7, low=0.1, high=3, default=0.1)
    amp = 0.3

    idxWf, idxWin, idxMod, out = dsp.pulsarstream(freq, length, pw, wf, win, mod, modr, modf, amp, idxWf, idxWin, idxMod)

    #out = dsp.taper(out, dsp.mstf(2))

    param.set('idxWf', idxWf)
    param.set('idxWin', idxWin)
    param.set('idxMod', idxMod)

    return out
