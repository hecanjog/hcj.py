from pippi import dsp
from pippi import tune
from hcj import fx

midi = {'lpd': 7, 'pc': 3}

def play(ctl):
    param = ctl.get('param')

    pc = ctl.get('midi').get('pc')
    pc.setOffset(111)

    lpd = ctl.get('midi').get('lpd')

    amp = pc.get(7)

    snds = ['sounds/melodica.wav', 'sounds/rhodes.wav', 'sounds/chime.wav', 'sounds/bell.wav', 'sounds/lap.wav']
    #snds = ['sounds/rhodes.wav']
    m = dsp.read(dsp.randchoose(snds)).data
    m = dsp.transpose(m, 0.125)
    m = dsp.transpose(m, dsp.randchoose([1, 1.5, 2, 3]) * 2**dsp.randint(0, 3))
    m = dsp.fill(m, dsp.stf(pc.get(15, low=0.125, high=2)))

    reverse = dsp.randchoose([True, False])
    numlayers = dsp.randint(10, 20)
    numgrains = dsp.randint(pc.geti(8, low=3, high=10), pc.geti(8, low=10, high=20))
    minlen = dsp.rand(10, 100)
    #lenranges = (dsp.rand(10, 20), dsp.rand(50, 1000))
    lenranges = (pc.get(15, low=10, high=50), pc.get(15, low=50, high=500))
    env = dsp.randchoose(['sine', 'hann', 'tri', 'vary'])

    #out = m
    out = fx.spider(m, numlayers, numgrains, minlen, lenranges, reverse)
    out = dsp.amp(out, amp)
    #out = dsp.env(out, 'sine')
    #out = dsp.alias(out)

    return out
