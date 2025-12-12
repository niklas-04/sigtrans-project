import wcslib as wcs

import argparse
import numpy as np
from scipy import signal
import sounddevice as sd

from parameters import Tb, dt, Wc

N = 7
fs = 1/dt


def demodulation_test():
    #Transmitted bits
    bits = np.array([1, 0 , 0, 0, 1, 1, 1, 0, 1 ,0, 1, 1, 0, 1, 0, 1, 0])
    xb = wcs.encode_baseband_signal(bits, Tb, fs=fs)


    tt = np.arange(0, xb.shape[0])*dt
    yI = xb * 2*np.cos(Wc*tt)
    yQ = xb * 2*np.sin(Wc*tt)



    # Demodulation
    #b_lp, a_lp = signal.cheby2(N, 31, 1100, btype = 'lowpass', fs=fs, output='ba')
    b_lp, a_lp = signal.butter(N, 1100, btype = 'lowpass', fs=fs, output='ba')

    yI = signal.lfilter(b_lp, a_lp, yI)
    yQ = signal.lfilter(b_lp, a_lp, yQ)

    yb = yI + 1J * yQ

    print(bits)
    br = wcs.decode_baseband_signal(yb, Tb, fs)
    print(br)
    data_rx = wcs.decode_string(br)
    print(f'Received: {data_rx} (no of bits: {len(br)}).')

demodulation_test()