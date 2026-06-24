"""
Plot band power features in real time
"""

import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_stream
from src.window import SlidingWindow
from src.bandpower import BandPower

FS = 250

streams = resolve_stream("type", "EEG")
inlet = StreamInlet(streams[0])

window = SlidingWindow(FS, FS // 4)
feature = BandPower(FS, (8, 12))

values = []

plt.ion()
fig, ax = plt.subplots()

while True:
    sample, _ = inlet.pull_sample()
    win = window.update(sample)

    if win is not None:
        bp = feature.compute(win)[0]
        values.append(bp)

        if len(values) > 50:
            values.pop(0)

        ax.clear()
        ax.plot(values)
        ax.set_title("Alpha Band Power (Channel 1)")
        plt.pause(0.01)

