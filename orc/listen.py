from pippi import dsp

midi = {'lpd': 7, 'pc': 3}

def play(ctl):
    lpd = ctl.get('midi').get('pc')
    param = ctl.get('param')
    pc = ctl.get('midi').get('pc')
    pc.setOffset(111)

    chord_index = param.get('chord_index', default=0)

    if lpd.get(36, default=1) < 1:
        dsp.log(lpd.get(36)) 
        param.set('chord_index', chord_index + 1)

    areas = ['high', 'pitch', 'mid', 'low']
    area = lpd.geti(6, low=0, high=len(areas), default=len(areas))
    if area == len(areas):
        area = dsp.randchoose(areas)
    else:
        area = areas[area]

    param.set('wash-area', area, throttle=1)

    return dsp.pad('', 0, dsp.mstf(100))
