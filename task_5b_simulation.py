import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import wcslib as wcs

# Importera dina parametrar
from parameters import fs, dt, Tb, Ac, Wc, fc

def main():
    # --- 1. SKAPA SIGNAL (Sändare) ---
    message = "Hello 5b"
    bits = wcs.encode_string(message)
    print(f"Simulating transmission of: '{message}'")

    # Skapa basband (xb)
    xb = wcs.encode_baseband_signal(bits, Tb, fs)
    
    # Modulera (xb -> xm)
    t = np.arange(len(xb)) * dt
    xm = xb * Ac * np.sin(Wc * t)

    # --- 2. BANDBEGRÄNSNING (Filter) ---
    # Designa filtret (Butterworth, Bandpass 900-1100 Hz)
    nyquist = fs / 2
    low = 900 / nyquist
    high = 1100 / nyquist
    b, a = signal.butter(4, [low, high], btype='band')

    # Den filtrerade signalen (xt) som "skickas"
    xt = signal.lfilter(b, a, xm)

    # --- 3. SIMULERA KANALEN (Detta är kärnan i Uppgift 5b) ---
    # simulate_channel lägger till brus och slumpmässig fördröjning
    # för att simulera att ljudet färdas genom luften.
    print("Simulating channel (adding noise and delay)...")
    yr = wcs.simulate_channel(xt, fs, 1)

    # --- 4. PLOTTA RESULTATET ---
    # Vi plottar en liten del av signalen för att se bruset
    plt.figure(figsize=(10, 6))
    
    # Plotta skickad signal
    plt.subplot(2, 1, 1)
    plt.plot(t[:1000], xt[:1000])
    plt.title("Skickad signal (xt) - Ren")
    plt.grid(True)

    # Plotta mottagen (simulerad) signal
    # Notera: yr är ofta längre pga fördröjning, så vi tar bara de första 1000
    plt.subplot(2, 1, 2)
    plt.plot(t[:1000], yr[:1000], color='orange')
    plt.title("Mottagen signal (yr) - Med brus och fördröjning")
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

    print("Simulation complete. 'yr' is now ready for the receiver steps.")

if __name__ == "__main__":
    main()