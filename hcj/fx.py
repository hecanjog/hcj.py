import subprocess
from pippi import dsp
import os

def rb(snd, length=None, speed=None, hz=None, interval=None, ratios=None, crisp=0, formant=False):
    pid = os.getpid()
    cmd = ['rubberband']

    # Time stretching
    if length is not None and dsp.flen(snd) != length and length > 0:
        cmd += [ '--duration %s' % dsp.fts(length) ] 

    # crisp setting
    cmd += [ '--crisp %s' % dsp.cap(crisp, 6, 0) ]

    # preserve formants
    if formant:
        cmd += [ '--formant' ]

    # pitch shift by speed
    if speed is not None:
        cmd += [ '--frequency %s' % speed ]

    # pitch shift by semitones
    if interval is not None:
        # TODO use pippi.tune ratios and calc frequency args
        cmd += [ '--pitch %s' % interval ]

    cmd = ' '.join(cmd) + ' /tmp/infile%s.wav /tmp/outfile%s.wav' % (pid, pid)

    dsp.write(snd, '/tmp/infile%s' % pid, cwd=False)

    with open(os.devnull, 'w') as devnull:
        p = subprocess.Popen(cmd, stdout=devnull, stderr=devnull, shell=True)
        p.wait()

    out = dsp.read('/tmp/outfile%s.wav' % pid).data

    return out

def stretch(snd, length=None, speed=None, interval=None, ratios=None, grain_size=60):
    original_length = dsp.flen(snd)

    if speed is not None:
        snd = dsp.transpose(snd, speed)
    elif interval is not None:
        if ratios is None:
            ratios = tune.terry
        
        speed = dsp.interval2speed(interval, ratios)
        snd = dsp.transpose(snd, speed) 

    current_length = dsp.flen(snd)

    if original_length != current_length or length is not None:
        grain_size = dsp.mstf(grain_size)

        numgrains = length / (grain_size / 2)
        block_size = original_length / numgrains
        left = []
        right = []

        original_position = 0

        count = 0
        while count <= numgrains:
            grain = dsp.cut(snd, original_position, grain_size)
            grain = dsp.env(grain, 'hann')

            if count == 1:
                right += [ dsp.pad('', 0, grain_size / 2) ]

            if count % 2 == 0:
                left += [ grain ]
            else:
                right += [ grain ]

            original_position += block_size
            count += 1

        left = ''.join(left) 
        right = ''.join(right) 

        snd = dsp.mix([left, right])

    return snd

