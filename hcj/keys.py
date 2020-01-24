from pippi import dsp
from pippi import tune
import fx, snds

from . import Tracks

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

def brass(length=22050, freq=220, amp=0.5, trill=None):
    pw = dsp.rand(0.25, 0.5)
    note = pulsar(length=length, freq=freq, pulsewidth=pw, amp=amp)
    noise = dsp.bln(length, dsp.rand(1000, 2000), dsp.rand(2000, 3000))
    noise = dsp.fill(noise, length)
    noise = fx.bend(noise, [ dsp.rand() for _ in range(dsp.randint(5, 10)) ], dsp.rand(0.01, 0.3))
    noise = dsp.amp(noise, dsp.rand(0.001, 0.002))
    noise = dsp.env(noise, 'tri')
    note = dsp.mix([ note, noise ])

    if trill is not None:
        unison = brass(length, freq, amp)

        try:
            slowest, fastest = trill
        except TypeError:
            slowest = int(trill * 1.5)
            fastest = int(trill * 0.5)

        track = Tracks()

        elapsed = 0
        count = 0
        readoffset = [0, 0]
        writeoffset = 0
        sndlength = dsp.randint(fastest, slowest)
        crosslength = fastest/2

        numpoints = dsp.randint(3, 6)
        points = [ dsp.randint(fastest, slowest) for _ in range(numpoints) ] 
        steps = length / fastest
        sndlengths = dsp.breakpoint(points, steps)

        while elapsed <= length:
            sndlength = int(sndlengths[count % steps])
            snd = [note, unison][count % 2]
            snd = dsp.cut(snd, readoffset[count % 2], sndlength)
            snd = dsp.env(snd, 'sine')
            snd = dsp.taper(snd, 20)

            track.add(snd, writeoffset)

            count += 1
            writeoffset += sndlength - crosslength
            readoffset[count % 2] += sndlength
            elapsed += sndlength

        note = track.mix()

    return note


def bell(length=22050, freq=220, amp=0.5):
    ding = dsp.read('/home/hecanjog/sounds/vibesc1.wav').data
    ding = dsp.amp(ding, dsp.rand(0.5, 0.8))
    ding = fx.bend(ding, [ dsp.rand() for _ in range(dsp.randint(5, 10)) ], dsp.rand(0, 0.02))

    bell = dsp.read('/home/hecanjog/sounds/tones/bellc.wav').data
    bell = dsp.amp(bell, dsp.rand(10, 50))
    bell = dsp.amp(bell, 0.3)

    rhodes = dsp.read('/home/hecanjog/sounds/tones/rhodes.wav').data
    rhodes = dsp.transpose(rhodes, 1.2)
    rhodes = dsp.pan(rhodes, dsp.rand())

    glade = dsp.read('/home/hecanjog/sounds/glade.wav').data
    numgs = dsp.randint(2, 6)

    gs = []
    for _ in range(numgs):
        g = dsp.rcut(glade, dsp.mstf(100, 500))
        g = dsp.amp(g, dsp.rand(0.2, 0.5))
        g = dsp.pan(g, dsp.rand())
        g = dsp.transpose(g, dsp.rand(0.15, 0.75))

        gs += [ g ]

    gs = dsp.mix(gs)
    gs = dsp.env(gs, 'phasor')

    clump = dsp.mix([ ding, gs, bell, rhodes ])

    clump = dsp.transpose(clump, freq / tune.ntf('c', octave=4))
    clump = dsp.fill(clump, length, silence=True)
    clump = dsp.env(clump, 'phasor')
    clump = dsp.amp(clump, amp)

    return clump
