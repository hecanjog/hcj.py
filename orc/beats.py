from pippi import dsp
from hcj import drums

midi = {'lpd': 3}

def play(ctl):
    lpd = ctl.get('midi').get('lpd')

    ksnd = dsp.read('/home/hecanjog/sounds/drums/Brushtap.wav').data
    hsnd = dsp.read('/home/hecanjog/sounds/drums/Shaker.wav').data

    beat = dsp.bpm2frames(90)
    length = beat * 4 

    hat =   'xx'
    kick =  'xx      '
    snare = '   x'
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
        h = dsp.amp(h, amp * 0.75)

        return h

    def makeKick(length, i, amp):
        return drums.sinekick(length, i, amp)

    def makeSnare(length, i, amp):
        s = ksnd
        s = dsp.pad(s, 0, length - dsp.flen(s))

        return s

    hats = drums.parsebeat(hat, 16, beat, length, makeHat, 25)
    kicks = drums.parsebeat(kick, 8, beat, length, makeKick, 10)
    snares = drums.parsebeat(snare, 8, beat, length, makeSnare, 0)

    out = dsp.mix([hats,kicks,snares])

    #out = dsp.drift(out, dsp.rand(0.5, 2))

    return out
