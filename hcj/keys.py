from pippi import dsp
from pippi import tune

def pulsar(freq, length=22050, drift=0.01, speed=0.5, amp=0.1, pulsewidth=None, env='flat', wf=None, mod=None):
    if wf is None:
        waveform = dsp.wavetable('sine2pi')
    else:
        waveform = wf

    window = dsp.wavetable('sine')

    if mod is None:
        mod = [ dsp.rand(0, 1) for i in range(10) ]

    modrange = dsp.rand(0, drift)
    modfreq = dsp.rand(0.0001, speed)
    pulsewidth = dsp.rand(0.1, 1) if pulsewidth is None else pulsewidth

    out = dsp.pulsar(freq, length, pulsewidth, waveform, window, mod, modrange, modfreq, amp)

    out = dsp.pan(out, dsp.rand())
    out = dsp.env(out, env)

    return out

def pulsars(chord, length=22050, drift=0.01, speed=0.5, amp=0.1, pulsewidth=None, env='flat', key='c', octave=3):
    freqs = tune.chord(chord, key, octave)
    return dsp.mix([ pulsar(freq, length, drift, speed, amp, pulsewidth, env) for freq in freqs ])

def pulsar_seq(chords, length=22050, drift=0.01, speed=0.5, amp=0.1, pulsewidth=None, env='flat', key='c', octave=3):
    chords = chords.split(' ')
    return dsp.cross([ pulsars(chord, length, drift, speed, amp, pulsewidth, env) for chord in chords ], 50, 80)

def yourlove(length=22050, i=0, bar=5, amp=0.5, chords=None, root='a', octave=3, maxdiv=4, mindiv=1):
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

    klen = length / dsp.randint(mindiv, maxdiv)

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

def rhodes(length=22050, freq=220.0, amp=0.5, wavetype='sine'):
    partials = [
            # Multiple, amplitude, duration
            [1, 0.6, 1.0], 
            [2, 0.25, 0.35], 
            [3, 0.08, 0.15],
            [4, 0.005, 0.04],
        ]

    layers = []
    for plist in partials:
        partial = dsp.tone(freq=plist[0] * freq, length=length, amp=plist[1], wavetype=wavetype)

        env_length = (length * plist[2] * 2) / 32 
        if env_length <= 2:
            env_length = 4

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

    out = dsp.mix([out, noise])
    out = dsp.amp(out, amp)

    return out

def chippy(length=22050, freq=220, amp=0.5):
    wfrm = dsp.wavetable('sine2pi', 512)
    wndw = dsp.wavetable('tri', 512)
    modw = [ 1 for u in range(256) ] + [ 0 for d in range(256) ]
    modr = 1
    modf = dsp.rand(10, 20)
    pw = dsp.rand()

    out = dsp.pulsar(freq, length, pw, wfrm, wndw, modw, modr, modf, amp)

    return out
