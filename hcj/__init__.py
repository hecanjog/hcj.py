from pippi import dsp
import fx

class Sampler:
    def __init__(self, snd, freq=220, direction='fw-loop', env='phasor', tails=False):
        self.snd = snd
        self.freq = freq
        self.direction = direction
        self.env = env
        self.tails = tails

    def makeTails(self, freq, length):
        freq *= 0.5
        harmonics = [ dsp.randint(1, 8) for _ in range(2, 4) ]
        layers = []
        for harmonic in harmonics:
            layer = dsp.tone(length, freq * harmonic, amp=dsp.rand(0.1, 0.3))
            layer = fx.penv(layer)
            layer = dsp.env(layer, 'sine')
            layers += [ layer ]

        layers = dsp.mix(layers)
        layers = dsp.amp(layers, dsp.rand(0.25, 1))

        return layers

    def play(self, freq, length):
        snd = dsp.transpose(self.snd, freq / self.freq)
        snd = dsp.taper(snd, 40)

        if self.direction == 'fw':
            snd = dsp.env(snd, self.env)
            snd = dsp.fill(snd, length, silence=True)

        if self.direction == 'fw-loop':
            snd = dsp.fill(snd, length, silence=False)
            snd = dsp.env(snd, self.env)

        if self.direction == 'fw-loop-rand':
            snd = dsp.env(snd, self.env)
            elapsed = 0
            sndout = ''
            while elapsed < length:
                sndout += dsp.pad(snd, 0, dsp.randint(0, dsp.flen(snd)))
                elapsed = dsp.flen(sndout)

            snd = dsp.fill(sndout, length, silence=False)

        if self.direction == 'fw-bw-loop':
            snd = dsp.fill(snd, length, silence=False)
            snd = dsp.env(snd, self.env)

        if self.tails:
            snd = dsp.mix([ snd, self.makeTails(freq, length) ])

        return snd


