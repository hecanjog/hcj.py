from pippi import dsp

def play(ctl):
    grains = dsp.randint(1, 100)

    o = ''
    for g in range(grains):
        length = dsp.stf(dsp.rand(0.001, 0.1))
        numpoints = dsp.randint(10, 30) 
        points = [0] + [ dsp.rand(-1, 1) for _ in range(numpoints) ] + [0]

        out = dsp.bln(length, 330, 330, 'tri')
        #out = dsp.am(out, dsp.tone(length, dsp.rand(10, 100)))
        out = dsp.env(out, 'random')
        out = dsp.pan(out, dsp.rand())
        out = dsp.amp(out, dsp.rand(0.1, 0.9))

        o += out

    out = dsp.env(o, 'random')
    out = dsp.pad(out, 0, dsp.stf(dsp.rand(0.1, 1)))

    return out
