from pippi import dsp
from pippi import tune
from hcj import synth

def play(ctl):
    param = ctl.get('param')
    key = param.get('key', default='d')
    chord = tune.fromdegrees([1,3,5,8], octave=6, root=key)
    lyrics = 'you guys this is singing'
    out = synth.sing(lyrics, chord)

    return out
