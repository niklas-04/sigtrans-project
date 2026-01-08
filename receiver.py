#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Receiver för Grupp 5 (Fixad version)
"""

import argparse
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
import sounddevice as sd
import wcslib as wcs

# Importera parametrar
from parameters import Tb, fs, fc, Wc

def main():
    parser = argparse.ArgumentParser(description='Receiver Group 5')
    parser.add_argument('-d', '--duration', help='recording duration', type=float, default=4.0)
    args = parser.parse_args()

    T_rec = args.duration
    
    # 1. Spela in
    print(f'Recording for {T_rec} s...')
    try:
        # sd.rec returnerar en array med shape (samples, channels)
        yr = sd.rec(int(T_rec * fs), samplerate=fs, channels=1, blocking=True)
        yr = yr[:, 0] # Platta ut till 1D
        print("Recording finished.")
    except Exception as e:
        print(f"Microphone error: {e}")
        return

    # --- DEBUG PLOT: KOLLA ATT MIKROFONEN FUNKAR ---
    if np.max(np.abs(yr)) < 0.001:
        print("\nVARNING: Signalen är nästan helt tyst (bara nollor)!")
        print("Kolla dina ljudinställningar i Linux (Settings -> Sound -> Input).")
    
    plt.figure(figsize=(10, 4))
    plt.plot(yr)
    plt.title("Rå inspelad signal (Innan filter)")
    plt.xlabel("Samples")
    plt.ylabel("Amplitud")
    plt.show() # Stäng fönstret för att fortsätta koden
    # -----------------------------------------------

    t = np.arange(len(yr)) / fs

    # 2. Bandpassfilter (Ta fram 900-1100 Hz)
    nyquist = fs / 2
    low = 900 / nyquist
    high = 1100 / nyquist
    apass = 1
    astop = 30
    
    b_bp, a_bp = signal.ellip(5, apass, astop, [low, high], btype='bandpass', analog=False, fs=fs, output='ba')
    
    ym = signal.lfilter(b_bp, a_bp, yr)

    # 3. IQ Demodulering
    # Multiplicera med 2*cos och 2*sin
    yI_d = ym * 2 * np.cos(Wc * t)
    yQ_d = ym * 2 * np.sin(Wc * t)

    # 4. Lågpassfilter (Ta bort höga frekvenser, behåll basbandet)
    # Basbandet är ca 1/Tb = 100 Hz. Vi filtrerar vid 200 Hz.
    lp_cutoff = 200 / nyquist
    b_lp, a_lp = signal.butter(4, lp_cutoff, btype='low')

    yI = signal.lfilter(b_lp, a_lp, yI_d)
    yQ = signal.lfilter(b_lp, a_lp, yQ_d)

    # Skapa komplex signal
    yb = yI + 1j * yQ

    # 5. Avkodning
    print("Attempting to decode...")
    try:
        # decode_baseband_signal hittar synkroniseringen själv
        br = wcs.decode_baseband_signal(yb, Tb, fs)
        text_rx = wcs.decode_string(br)
        
        print("\n--------------------------------")
        print(f"Bits detected: {len(br)}")
        print(f"RECEIVED MESSAGE: {text_rx}")
        print("--------------------------------\n")
        
    except Exception as e:
        print(f"Decoding failed (signal might be too weak or noisy): {e}")

if __name__ == "__main__":    
    main()