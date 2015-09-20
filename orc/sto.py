from pippi import dsp

def play(ctl):
    def stream(length, numsegments, freq):

        out = []
        seglength = dsp.randint(100, 300)
        points = [ dsp.rand(-1, 1) for _ in range(dsp.randint(10, 20)) ]

        for _ in range(numsegments):
            seglength = dsp.cap(seglength + dsp.randint(-5, 5), 1000, 100)
            points = [ dsp.cap(p + dsp.randint(-0.1, 0.1), 1, -1) for p in points ]

            out += dsp.breakpoint([0] + points + [0], seglength)

        print len(out), freq, length

        out = dsp.ctone(freq, dsp.stf(length), out, dsp.rand(0.1, 0.5))
        #out = dsp.env(out, 'random')

        return out

    numstreams = dsp.randint(20, 30)
    out = ''

    for _ in range(numstreams):
        length = dsp.rand(100, 500) / 1000.0
        numsegments = dsp.randint(100, 200)
        freq = dsp.rand(200, 1000)
        out += stream(length, numsegments, freq)

    #out = dsp.env(out, 'random')

    return out
