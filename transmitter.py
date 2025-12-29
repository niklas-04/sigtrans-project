#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transmitter för Grupp 5 (Fixad version)
"""

import argparse
import numpy as np
from scipy import signal
import sounddevice as sd
import wcslib as wcs

# Importera parametrar
from parameters import Tb, Ac, fs, fc, Wc

def main():
    parser = argparse.ArgumentParser(description='Transmitter Group 5')
    parser.add_argument('-b', '--binary', help='message is binary', action='store_true')
    parser.add_argument('message', help='message to transmit', nargs='?', default='Hello World!')
    args = parser.parse_args()

    data = args.message

    # 1. Konvertera till bitar
    if args.binary:
        bs = np.array([int(bit) for bit in data])
    else:
        bs = wcs.encode_string(data)

    print(f'Sending: "{data}" ({len(bs)} bits, {len(bs)*Tb:.2f} s)')

    # 2. Skapa Baseband-signal
    # fs måste skickas med här för att pulserna ska bli rätt längd i samples
    xb = wcs.encode_baseband_signal(bs, Tb, fs)

    # 3. Modulering (Mix upp till 1000 Hz)
    t = np.arange(len(xb)) / fs
    carrier = Ac * np.sin(Wc * t)
    xm = xb * carrier

    # 4. Bandpassfilter (900-1100 Hz)
    # Vi använder Butterworth ordning 4 för stabilitet
    nyquist = fs / 2
    low = 900 / nyquist
    high = 1100 / nyquist
    b, a = signal.butter(4, [low, high], btype='band')
    
    xt = signal.lfilter(b, a, xm)

    # 5. Förbered för uppspelning (Viktigt fix!)
    # Lägg till tystnad före och efter
    silence = np.zeros(int(0.5 * fs))
    xt_out = np.concatenate((silence, xt, silence))

    # Gör till stereo (men tyst i ena kanalen)
    xt_stereo = np.stack((xt_out, np.zeros_like(xt_out)), axis=1)

    # --- NORMALISERING (Fixar "Overflow" varningen) ---
    # Ljudkortet klarar max 1.0. Er signal är ca 1.41.
    max_val = np.max(np.abs(xt_stereo))
    if max_val > 1.0:
        print(f"Info: Signal amplitude {max_val:.2f} > 1.0. Normalizing...")
        xt_stereo = xt_stereo / max_val
    # --------------------------------------------------

    print("Playing signal...")
    try:
        sd.play(xt_stereo, fs, blocking=True)
        print("Done.")
    except Exception as e:
        print(f"Playback error: {e}")

if __name__ == "__main__":    
    main()