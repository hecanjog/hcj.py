from pippi import dsp
from pippi import tune
from hcj import fx

midi = {'lpd': 7, 'pc': 3}

def play(ctl):
    param = ctl.get('param')

    #lpd = ctl.get('midi').get('lpd')
    #pc = ctl.get('midi').get('pc')
    #pc.setOffset(111)

    #r = dsp.read('sounds/roll.wav').data
    r = dsp.read('sounds/pills.wav').data
    r = dsp.fill(r, dsp.stf(3))
    #tr = pc.get(10, low=0.125, high=4)
    tr = dsp.rand(0.125, 4)
    r = dsp.transpose(r, dsp.rand(tr * 0.25, tr * 2))
    #r = dsp.amp(r, pc.get(1, low=0, high=10))
    r = dsp.amp(r, dsp.rand(0, 10))

    reverse = dsp.randchoose([True, False])
    #numgrains = pc.geti(2, low=5, high=20) 
    numgrains = dsp.randint(5, 20)
    #numlayers = pc.geti(3, low=5, high=50) 
    numlayers = dsp.randint(5, 50)
    #minlen = lpd.get(9, low=10, high=100)
    minlen = dsp.rand(10, 100)
    #lenranges = (lpd.get(9, low=10, high=50), lpd.get(9, low=50, high=500))
    lenranges = (dsp.rand(10, 50), dsp.rand(50, 500))


    out = fx.spider(r, numlayers, numgrains, minlen, lenranges, reverse)
    #out = dsp.mix([out, dsp.env(r, 'sine')])

    return out
