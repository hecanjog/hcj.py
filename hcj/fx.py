import subprocess
from pippi import dsp
import os

def rb(snd, speed=None, hz=None, interval=None, ratios=None, length=None, crisp=0, formant=True):
    pid = os.getpid()
    cmd = ['rubberband']

    # Time stretching
    if length is not None and dsp.flen(snd) != length and length > 0:
        cmd += [ '--duration %s' % dsp.fts(length) ] 

    cmd = ' '.join(cmd) + ' /tmp/infile%s.wav /tmp/outfile%s.wav' % (pid, pid)

    dsp.write(snd, '/tmp/infile%s' % pid, cwd=False)

    with open(os.devnull, 'w') as devnull:
        p = subprocess.Popen(cmd, stdout=devnull, stderr=devnull, shell=True)
        p.wait()

    out = dsp.read('/tmp/outfile%s.wav' % pid).data

    return out
