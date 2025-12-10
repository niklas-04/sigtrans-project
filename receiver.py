#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Receiver template for the wireless communication system project in Signals and
transforms

2022-present -- Roland Hostettler <roland.hostettler@angstrom.uu.se>
"""

import argparse
import numpy as np
from scipy import signal
import sounddevice as sd

import wcslib as wcs

# TODO: Add relevant parametrs to parameters.py
from parameters import Tb, dt # ...

def main():
    parser = argparse.ArgumentParser(
        prog='receiver',
        description='Acoustic wireless communication system -- receiver.'
    )
    parser.add_argument(
        '-d',
        '--duration',
        help='receiver recording duration',
        type=float,
        default=10
    )
    args = parser.parse_args()

    # Set parameters
    T = args.duration

    # Receive signal
    print(f'Receiving for {T} s.')
    yr = sd.rec(int(T/dt), samplerate=1/dt, channels=1, blocking=True)
    yr = yr[:, 0]           # Remove second channel
    #yr = h(t) * xb + vr(t)  # Received signal model
    #yr = |H(wc)|xm(t-tr) + v(t)
    # TODO: Implement demodulation, etc. here
    # ...   
    f = 1000
    Tb = 25/f
    dt = 1/ 22050
    xb = wcs.encode_baseband_signal(yr, Tb)
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

    _, yb, _= signal.lsim(H, yd, t)


    xasad = wcs.decode_baseband_signal(yd, Tb)
    # Baseband signal
    # yb = ...

    # Symbol decoding
    # TODO: Adjust fs (lab 2 only, leave untouched for lab 1 unless you know what you are doing)
    br = wcs.decode_baseband_signal(yb, Tb, 1/dt)
    data_rx = wcs.decode_string(br)
    print(f'Received: {data_rx} (no of bits: {len(br)}).')


if __name__ == "__main__":    
    main()
