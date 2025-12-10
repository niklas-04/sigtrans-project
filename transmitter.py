#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transmitter template for the wireless communication system project in Signals and
transforms

For plain text inputs, run:
$ python3 transmitter.py "Hello World!"

For binary inputs, run:
$ python3 transmitter.py -b 010010000110100100100001

2022-present -- Roland Hostettler <roland.hostettler@angstrom.uu.se>
"""

import argparse
import numpy as np
from scipy import signal
import sounddevice as sd

import wcslib as wcs

# TODO: Add relevant parameters to parameters.py
from parameters import Tb, Ac, dt # ...


def main():
    parser = argparse.ArgumentParser(
        prog='transmitter',
        description='Acoustic wireless communication system -- transmitter.'
    )
    parser.add_argument(
        '-b',
        '--binary',
        help='message is a binary sequence',
        action='store_true'
    )
    parser.add_argument('message', help='message to transmit', nargs='?')
    args = parser.parse_args()

    if args.message is None:
        args.message = 'Hello World!'

    # Set parameters
    data = args.message

    # Convert string to bit sequence or string bit sequence to numeric bit
    # sequence
    if args.binary:
        bs = np.array([bit for bit in map(int, data)])
    else:
        bs = wcs.encode_string(data)
    
    # Transmit signal
    print(f'Sending: {data} (no of bits: {len(bs)}; message duration: {np.round(len(bs)*Tb, 1)} s).')

    # Encode baseband signal
    # TODO: Adjust fs (lab 2 only, leave untouched for lab 1 unless you know what you are doing)
    xb = wcs.encode_baseband_signal(bs, Tb, 1/dt)  #fs = 1 / dt 

    # TODO: Implement transmitter code here
    # xt = ...
    # First we Baseband encode the signal
    # Second we Modulate the signal
    tt = np.arange(0, xb.shape[0])*dt
    xt = np.zeros_like(xb)
    
    for i in range(len(xt)):
        xt[i] = xb[i] * Ac * np.sin(2*1000*np.pi*tt[i])
    # xt = xb * Ac * np.sin(2*1000*np.pi* tt)

    N = 4 # order for the filter
    wn = [900, 1100] # critical freq for filter which should be from 900 to 1100
    btype = "bandpass"
    fs = 1/dt # freq sampling

    # we bandlimit it our freq range to the specification from the appendix which is from 900 - 1100 Hz 
    b, a =  signal.butter(N, wn, btype, fs, output='ba')
    xt = signal.lfilter(b, a, xt)

    # Ensure the signal is mono, then play through speakers
    xt = np.stack((xt, np.zeros(xt.shape)), axis=1)
    sd.play(xt, 1/dt, blocking=True)


if __name__ == "__main__":    
    main()
