from pippi import dsp
from pippi import tune

def yourlove(length=22050, i=0, bar=5, amp=0.5, chords=None, root='a', octave=3):
    """ Inspired by Terre """
    wav = dsp.wavetable('sine2pi', 512)
    win = dsp.wavetable('sine', 512)
    mod = dsp.wavetable('phasor', 512)

    if chords is None:
        chords = [
            [5, 7, 1],
            [5, 4, 1],
            [3, 2, 1, 6],
        ]

    pw = dsp.rand(0.1, 1)

    notes = chords[i % len(chords)]
    notes = tune.fromdegrees(notes, root=root, octave=octave)

    klen = length / dsp.randint(1, 4)

    amp = dsp.rand(0.3, 0.5)

    mFreq = dsp.rand(0.5, 1.0) / dsp.fts(klen)

    layers = []

    for note in notes:
        k = dsp.pulsar(note, klen, pw, wav, win, mod, 0.005, mFreq, amp) 
        k = dsp.env(k, 'sine')
        k = dsp.pan(k, dsp.rand())
        k = dsp.pad(k, 0, length - klen)

        layers += [ k ]

    out = dsp.mix(layers)

    return out

def rhodes(length=22050, freq=220.0, amp=0.5):
    partials = [
            # Multiple, amplitude, duration
            [1, 0.6, 1.0], 
            [2, 0.25, 0.35], 
            [3, 0.08, 0.15],
            [4, 0.005, 0.04],
        ]

    layers = []
    for plist in partials:
        partial = dsp.tone(freq=plist[0] * freq, length=length, amp=plist[1] * amp)

        env_length = (length * plist[2] * 2) / 32 
        wtable = dsp.wavetable('hann', int(env_length))
        wtable = wtable[int(env_length / 2):]
        wtable.extend([0 for i in range(length - len(wtable))])
        
        partial = dsp.split(partial, 32)
        partial = [ dsp.amp(partial[i], wtable[i]) for i in range(len(partial)) ]
        layer = ''.join(partial)

        layers += [ layer ]

    out = dsp.mix(layers)
    noise = dsp.amp(dsp.bln(dsp.flen(out) * 2, 2000, 20000), 0.005)
    noise = dsp.fill(noise, dsp.flen(out))

    return dsp.mix([out, noise])

