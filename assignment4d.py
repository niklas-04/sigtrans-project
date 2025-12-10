import wcslib as wcs
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt


alpha = 400*np.pi
num = np.array([alpha**2])
den  = np.array([1, alpha, alpha**2])


H = signal.TransferFunction(num, den)

w, mag, phase = H.bode()

fig, ax4 = plt.subplots(2,1)
ax4[0].semilogx(w, mag)
# ax4[0].ylabel("|H(w)|")
ax4[0].set_xlabel("w")
ax4[0].set_ylabel("|H(w)|")

ax4[1].set_ylabel("Phase ( < H(w) )")
ax4[1].set_xlabel("w")
ax4[1].semilogx(w, phase)

plt.show()
plt.show()
plt.show()
