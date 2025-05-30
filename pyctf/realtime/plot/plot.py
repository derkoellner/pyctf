import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

class Scope(object):

    def __init__(self, ax, maxt=2, dt=0.02):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.ymin = 1000000
        self.ymax = -1000000
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-.1, 1.1)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:   # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.ymin = np.min((self.ymin, y))
        self.ymax = np.max((self.ymax, y))
        if self.ymax > self.ymin:
            self.ax.set_ylim(self.ymin, self.ymax)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,

def emitter(x=0):
    'return a random value with probability p, else 0'

    while True:
        x = x + 1
        #yield math.sin(math.radians(x))
        yield np.random.random()

# Fixing random state for reproducibility
np.random.seed(19680801)

fig, ax = plt.subplots()
scope = Scope(ax)

# pass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, emitter, interval=2, blit=True)

#plt.show()
