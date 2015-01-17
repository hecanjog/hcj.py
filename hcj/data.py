from pippi import dsp

class Logistic():
    def __init__(self, r=3.6, x=0.5, size=100, pointer=0, normalize=True):
        self.data = dsp.logistic(r, x, size)

        if normalize:
            maxval = max(self.data)
            minval = min(self.data)

            self.data = [ (v - minval) / (maxval - minval) for v in self.data ]

        self.pointer = pointer
        self.limit = size - 1

    def next(self):
        val = self.data[self.pointer % self.limit]
        self.pointer += 1
        return val

    def get(self, low=0.0, high=1.0, trunc=False):
        val = self.next() * (high - low) + low

        if trunc:
            val = int(round(val))

        return val

    def shuffle(self, items):
        shuffled = []

        while items:
            chosen = self.get(0, len(items) - 1, trunc=True)
            shuffled += [ items.pop(chosen) ]

        return shuffled

    def choose(self, items):
        return items[self.get(0, len(items) - 1, trunc=True)]


