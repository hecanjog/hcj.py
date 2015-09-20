from pippi import dsp, tune
from hcj import snds, keys

def play(ctl):
    freq = tune.ntf(dsp.randchoose(['eb']), octave=dsp.randint(0,2))

    synth = keys.rhodes(dsp.stf(4), freq)

    s = dsp.vsplit(synth, dsp.mstf(50), dsp.mstf(2000))
    s = dsp.randshuffle(s)
    #s = [ dsp.alias(ss) for ss in s ]
    s = [ dsp.amp(ss, dsp.rand(0.5, 0.75)) for ss in s ]
    s = [ dsp.pan(ss, dsp.rand(0, 1)) for ss in s ]
    s = ''.join(s)
    s = dsp.fill(s, dsp.flen(synth))

    s2 = dsp.vsplit(synth, dsp.mstf(150), dsp.mstf(1500))
    s2 = dsp.randshuffle(s2)
    s2 = [ dsp.transpose(ss, dsp.randchoose([1,1.5,2,3,4,8])) for ss in s2 ]
    s2 = [ dsp.env(ss, 'phasor') for ss in s2 ]
    s2 = ''.join(s2)


    out = dsp.mix([ s, s2 ])

    out = dsp.amp(out, 1.5)

    out = dsp.transpose(out, 1.01) 
#synth = dsp.fill(synth, dsp.flen(main))

#out = synth

    return out
