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
from parameters import Tb, dt, Ac, Wc# ...

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
    #Band limiation
    N = 4 # order for the filter
    wn = [900, 1100] # critical freq for filter which should be from 900 to 1100
    btype = "bandpass"
    fs = 1/dt # freq sampling

    # we bandlimit it our freq range to the specification from the appendix which is from 900 - 1100 Hz 
    b, a =  signal.butter(N, wn, btype, fs=fs, output='ba')
    yr = signal.lfilter(b, a, yr)
    
    tt = np.arange(0, yr.shape[0])*dt
    yI = yr * 2*np.cos(Wc*tt)
    yQ = yr * 2*np.sin(Wc*tt)
    
    # Demodulation
    b_lp, a_lp = signal.butter(N, 900, "lowpass", fs=fs , output="ba")
    yI = signal.lfilter(b_lp, a_lp, yI)
    yQ = signal.lfilter(b_lp, a_lp, yQ)
    
    yb = yI + 1J * yQ

    # Symbol decoding
    # TODO: Adjust fs (lab 2 only, leave untouched for lab 1 unless you know what you are doing)
    br = wcs.decode_baseband_signal(yb, Tb, 1/dt)
    data_rx = wcs.decode_string(br)
    print(f'Received: {data_rx} (no of bits: {len(br)}).')


if __name__ == "__main__":    
    main()
