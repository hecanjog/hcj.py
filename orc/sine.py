from pippi import dsp
from pippi import tune

def play(ctl):
    out = dsp.tone(dsp.stf(6), freq=80, amp=1)
    out = dsp.env(out, 'phasor')

    return out
