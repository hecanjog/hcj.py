from pippi import dsp
from hcj import drums

midi = {'lpd': 3}

def play(ctl):
    lpd = ctl.get('midi').get('lpd')

    ssnd = dsp.read('/home/hecanjog/sounds/drums/Tinysd.wav').data
    hsnd = dsp.read('/home/hecanjog/sounds/drums/Shaker.wav').data
    ksnd = dsp.read('/home/hecanjog/sounds/drums/Drybd2.wav').data

    beat = dsp.bpm2frames(120)
    length = beat * 4 

    hat =   'xx'
    kick =  'x '
    #kick = ''.join([ dsp.randchoose([' ', 'x']) for s in range(dsp.randint(3, 5))])
    #hat = ''.join([ dsp.randchoose([' ', 'x']) for s in range(dsp.randint(3, 5))])
    if dsp.rand() > 0.75:
        snare = ''.join([ dsp.randchoose([' ', 'x']) for s in range(dsp.randint(6, 8))])
    else:
        snare =  '  x '
    #        x.-.x.-.x.-.x.-.x.-.

    def makeHat(length, i, amp):
        """
        h = dsp.tone(dsp.mstf(dsp.rand(1, 3)), dsp.rand(11900, 12000))
        h = dsp.env(h, 'phasor')
        h = dsp.pad(h, 0, length - dsp.flen(h))
        h = dsp.amp(h, amp * 0.25)
        """

        #h = dsp.cut(hsnd, 0, dsp.mstf(dsp.rand(3, 10)))
        h = hsnd
        h = dsp.env(h, 'phasor')
        h = dsp.pad(h, 0, length - dsp.flen(h))
        #h = dsp.amp(h, amp * 0.75)

        return h

    def makeKick(length, i, amp):
        #k = drums.sinekick(length, i, amp)
        k = dsp.fill(ksnd, length, silence=True)
        k = dsp.amp(k, 2)

        return k

    def makeSnare(length, i, amp):
        s = ssnd
        s = dsp.amp(s, 10)
        s = dsp.transpose(s, dsp.rand(0.8, 1))
        s = dsp.fill(s, length, silence=True)
        ss = dsp.drift(s, dsp.rand(0.001, 0.1))
        s = dsp.mix([s, ss])

        return s

    hats = drums.parsebeat(hat, 16, beat, length, makeHat, 25)
    kicks = drums.parsebeat(kick, 8, beat, length, makeKick, 10)
    snares = drums.parsebeat(snare, 8, beat, length, makeSnare, 0)

    out = dsp.mix([hats,kicks,snares])

    out = dsp.split(out, beat)
    out = dsp.randshuffle(out)
    out = ''.join(out)

    out = dsp.amp(out, 2)

    #out = dsp.drift(out, dsp.rand(0.5, 2))

    return out
