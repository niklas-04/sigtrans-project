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

yd = xb * xc * xc 

alpha = 400*np.pi
num = np.array([alpha**2])
den  = np.array([1, alpha, alpha**2])


H = signal.TransferFunction(num, den)

w, mag, phase = H.bode()

_, yb, _= signal.lsim(H, yd, t)


xasad = wcs.decode_baseband_signal(yd, Tb)




print(bits)
print(xasad)
