import numpy as np

class SummedAreaTable(np.ndarray):
    
    def __new__(cls, a):
        obj = np.asarray(a.cumsum(1).cumsum(0)).view(cls)
        return obj

    def __init__(self, a):
        self.zero = np.zeros_like(np.ndarray.__getitem__(self, (0,0)))

    def __array_finalize__(self, obj):
        if obj is None: return

    def __setitem__(self, i, d):
        x,y = i
        p_x = max(x-1,  0)
        p_y = max(y-1,  0)
        a = np.ndarray.__getitem__(self, (x, p_y)) if p_y != y else self.zero
        b = np.ndarray.__getitem__(self, (p_x, y)) if p_x != x else self.zero
        np.ndarray.__setitem__(self, i, a+b+d)

    def mean(self, i):
        x, y = i
        a = np.ndarray.__getitem__(self, (x.stop, y.stop))
        b = np.ndarray.__getitem__(self, (x.stop, y.start))
        c = np.ndarray.__getitem__(self, (x.start, y.stop))
        d = np.ndarray.__getitem__(self, (x.start, y.start))
        w = x.stop - x.start
        h = y.stop - y.start
        return (a - b - (c - d)) / (h*w)
