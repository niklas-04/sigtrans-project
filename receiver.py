#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Receiver template for the wireless communication system project in Signals and
transforms

2022-present -- Roland Hostettler <roland.hostettler@angstrom.uu.se>
"""

import argparse
from matplotlib import pyplot as plt
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
    # yr = h(t) * xb + vr(t)  # Received signal model
    # yr = |H(wc)|xm(t-tr) + v(t)
    # TODO: Implement demodulation, etc. here
    # ...
    # Band limiation
        # Band limitation
    N = 10
    wn = [900, 1100]   # Hz
    btype = "bandpass"
    fs = 1/dt

    b, a = signal.butter(N, wn, btype=btype, fs=fs, output='ba')

    # Correct digital frequency response
    w, h = signal.freqz(b, a, worN=4096, fs=fs)

    fig, ax = plt.subplots(2,1)
    ax[0].semilogx(w, 20*np.log10(np.abs(h)))
    ax[0].set_title("Magnitude response")
    ax[0].set_xlim(800, 1200)
    ax[0].set_ylim(-100, 1)

    ax[1].semilogx(w, np.unwrap(np.angle(h)))
    ax[1].set_title("Phase response")
    ax[1].set_xlim(800, 1200)

    plt.show()

    yr = signal.lfilter(b, a, yr)

    tt = np.arange(0, yr.shape[0])*dt
    yI = yr * 2*np.cos(Wc*tt)
    yQ = yr * 2*np.sin(Wc*tt)

    # Demodulation

    cutoff = 40  # Hz (optimal for Tb = 0.1)
    b_lp, a_lp = signal.butter(N, cutoff, "lowpass", fs=fs , output="ba")
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
