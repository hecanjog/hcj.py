from pippi import dsp
from hcj import fx

def play(ctl):
    snd = dsp.read('../sounds/guitarpluck.wav').data

    #out = fx.rb(snd, interval=dsp.randint(0, 8) * 2, length=dsp.stf(0.25), formant=False)
    out = dsp.stretch(snd, length=dsp.stf(0.2), grain_size=120)

    return out
