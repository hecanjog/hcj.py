from pippi import dsp
import subprocess
import math

def speak(lyrics, speed=0.5, voice='icelandic', pitch=1):
    speed = int(speed * 370 + 80)

    pitch = math.floor(pitch * 99.0)

    cmd = 'espeak -s %s -a 200 -v %s -p %s --stdout -z "%s"' % (speed, voice, pitch, lyrics)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out = dsp.transpose(out, 0.5, 1)
    out = dsp.stereo(out)

    return out

def sing(lyrics, freqs, speed=0, voice='english'):
    """ sing it mad slow in chords """
    out = speak(lyrics, speed, voice)
    layers = []

    for freq in freqs:
        layer = dsp.transpose(out, 0.25)
        layer = dsp.pine(layer, dsp.flen(layer) * 4, freq)

        slop = int(dsp.flen(layer) * 0.12)
        layer = dsp.cut(layer, slop, dsp.flen(layer) - (slop * 2))

        layer = dsp.transpose(layer, 4)
        layer = dsp.pan(layer, dsp.rand())
        layer = dsp.amp(layer, 0.5)
        layers += [ layer ]

    out = dsp.mix(layers)

    return out
