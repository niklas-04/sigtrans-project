import wcslib as wcs

import argparse
import numpy as np
from scipy import signal
import sounddevice as sd

from parameters import Tb, dt, Wc, Ac

N = 7
fs = 1/dt

def string_to_bits(s):
    bits = []
    for char in s:
        binary = format(ord(char), '08b')
        bits.extend(int(b) for b in binary)
    return bits


def demodulation_test():

    string = input("Input: \n")
    bitsString = string_to_bits(string)


    #Transmitted bits
    xb = wcs.encode_baseband_signal(bitsString, Tb, fs=fs)

    tt = np.arange(0, xb.shape[0])*dt

    #Modulation
    xt = np.zeros_like(xb)
    for i in range(len(xt)):
        xt[i] = xb[i] * Ac * np.sin(Wc * tt[i])


    #Demodulation
    yI = xt * 2*np.cos(Wc*tt)
    yQ = xt * 2*np.sin(Wc*tt)


    #Filtering away artifact frequency at 2000 Hz
    #b_lp, a_lp = signal.cheby2(N, 31, 1100, btype = 'lowpass', fs=fs, output='ba')
    b_lp, a_lp = signal.butter(N, 200, btype = 'lowpass', fs=fs, output='ba')

    yI = signal.lfilter(b_lp, a_lp, yI)
    yQ = signal.lfilter(b_lp, a_lp, yQ)

    yb = yI + 1J * yQ

    br = wcs.decode_baseband_signal(yb, Tb, fs)
    print(br)
    data_rx = wcs.decode_string(br)
    print(f'Received: {data_rx} (no of bits: {len(br)}).')
    

demodulation_test()