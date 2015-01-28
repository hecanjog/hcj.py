from pippi import dsp
from pippi import tune
from hcj import synth

def play(ctl):
    param = ctl.get('param')
    key = param.get('key', default='d')
    chord = tune.fromdegrees([1,3,5,8], octave=2, root=key)
    lyrics = 'hello there'
    out = synth.sing(lyrics, chord)
    dsp.write(out, 'singy')

    return out
