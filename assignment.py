import wcslib as wcs
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

Tb = 25/1000
dt = 1 / 22050
bits = [1, 0, 1, 0, 1, 1, 1, 0, 1 ,0]
print("ts")
xb = wcs.encode_baseband_signal(bits, Tb, 1000)
# t = np.arange(0, xb.shape[0])*dt
t = np.arange(0, 10 * Tb, dt)
print("hej")
fig, ax = plt.subplots()
ax.plot(t, xb, label="x1(t)")

ax.set_xlabel("Time (s)")
ax.set_ylabel("x(t)")

ax.legend()

ax.set_xlim(0, 10 * 10**-3)
ax.set_ylim(-1.1, 1.1)

plt.show()
