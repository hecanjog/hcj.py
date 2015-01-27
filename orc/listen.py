from pippi import dsp

midi = {'lpd': 3}

def play(ctl):
    lpd = ctl.get('midi').get('lpd')
    param = ctl.get('param')

    chord_index = param.get('chord_index', default=0)

    if lpd.get(36, default=1) < 1:
        dsp.log(lpd.get(36)) 
        param.set('chord_index', chord_index + 1)

    return dsp.pad('', 0, dsp.mstf(100))
