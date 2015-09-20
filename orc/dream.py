from pippi import dsp
from pippi import tune

def play(ctl):
    bell = dsp.read('sounds/bell.wav').data
    bell = dsp.transpose(bell, dsp.randchoose([0.125, 0.25, 0.5, 1, 2]))

    chime = dsp.read('sounds/chime.wav').data
    chime = dsp.transpose(chime, dsp.randchoose([0.125, 0.25, 0.5, 1, 2]))

    note = dsp.mix([ bell, chime ])

    def makeNote(length, note, degree=1):
        speed = tune.terry[tune.major[degree - 1]]
        speed = speed[0] / speed[1]

        note = dsp.transpose(note, speed)
        note = dsp.fill(note, length, silence=True)
        note = dsp.taper(note, dsp.mstf(10))

        return note

    scale = [ dsp.randchoose([1,5,6]) for s in range(4) ] * 3

    out = ''.join([ makeNote(dsp.mstf(dsp.rand(10, 500)), note, d) for d in scale ])

    return out
