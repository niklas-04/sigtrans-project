import wcslib as wcs
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

f = 1000
Tb = 25/f
dt = 1/ 22050
bits = np.array([1, 0 , 1, 0, 1, 1, 1, 0, 1 ,0])
xb = wcs.encode_baseband_signal(bits, Tb)
t = np.arange(0, xb.shape[0])*dt
Ac = 2**0.5
xc = np.zeros_like(xb)
for i in range(len(xc)):
    xc[i] = Ac * np.sin(2*np.pi*f * t[i])

xm = xb * xc
#t = np.arange(0, 10 * Tb, dt)
fig, ax = plt.subplots()
ax.plot(t, xm, label="x1(t)")
ax.set_xlabel("Time (s)")
ax.set_ylabel("x(t)")

ax.set_xlim(0, 4*Tb)

ax.legend()


plt.show()
