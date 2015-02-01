from pippi import dsp
from hcj import fx

def play(ctl):
    snd = dsp.read('/home/hecanjog/sounds/guitarpluck.wav').data

    #out = fx.rb(snd, interval=dsp.randint(0, 8) * 2, length=dsp.stf(0.25), formant=False)
    snd = dsp.transpose(snd, 0.968)
    out = dsp.stretch(snd, length=dsp.stf(dsp.rand(12, 15)), grain_size=120)
    out = dsp.env(out, 'hann')

    return out
