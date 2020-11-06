import random as rnd
import numpy as np

class Map:
    def __init__(self, dim):
        self.probabilities = np.full([dim, dim], float(1/dim**2),dtype=float)
        self.landscapes = np.zeros([dim, dim], dtype=float)
        self.target = (-1,-1)
        self.dim = dim

    def set_map(self):
        i = 0
        while i < self.dim:
            j = 0
            while j < self.dim:
                landscape = rnd.randint(0, 9)
                if landscape < 2:
                    self.landscapes[i][j] = 0.1
                elif landscape < 5:
                    self.landscapes[i][j] = 0.3
                elif landscape < 8:
                    self.landscapes[i][j] = 0.7
                else:
                    self.landscapes[i][j] = 0.9
                j += 1
            i += 1
        self.target = (rnd.randint(0, self.dim - 1), rnd.randint(0, self.dim - 1))

a = Map(3)
a.set_map()
print(a.landscapes)
print(a.target)