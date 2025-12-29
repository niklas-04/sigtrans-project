import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import wcslib as wcs

# Importera parametrarna för Grupp 5
from parameters import fs, dt, Tb, Ac, Wc

def main():
    # ==========================================
    # DEL 1: SÄNDARE (Transmitter)
    # ==========================================
    message = "Hello Group 5!"
    print(f"1. Transmitting: '{message}'")

    # Koda till bitar och basband
    bits_tx = wcs.encode_string(message)
    xb = wcs.encode_baseband_signal(bits_tx, Tb, fs)

    # Modulera (xb -> xm)
    t_tx = np.arange(len(xb)) * dt
    xm = xb * Ac * np.sin(Wc * t_tx)

    # Bandpassfilter (Sändare) - 900-1100 Hz
    nyquist = fs / 2
    b_bp, a_bp = signal.butter(4, [900/nyquist, 1100/nyquist], btype='band')
    xt = signal.lfilter(b_bp, a_bp, xm)

    # ==========================================
    # DEL 2: KANAL (Simulation - Uppgift 5b)
    # ==========================================
    print("2. Simulating Channel (Adding noise & delay)...")
    # Kanal 1 för Grupp 5
    yr = wcs.simulate_channel(xt, fs, 1)

    # ==========================================
    # DEL 3: MOTTAGARE (Receiver - Uppgift 5c)
    # ==========================================
    print("3. Receiving and Processing...")

    # A. Bandbegränsning (Samma filter som sändaren för att ta bort brus)
    ym = signal.lfilter(b_bp, a_bp, yr)

    # B. IQ-Demodulering
    # Vi måste skapa en tidsvektor som är lika lång som den mottagna signalen (yr)
    t_rx = np.arange(len(ym)) * dt
    
    # Multiplicera med 2*cos och 2*sin
    yI_temp = ym * 2 * np.cos(Wc * t_rx)
    yQ_temp = ym * 2 * np.sin(Wc * t_rx)

    # C. Lågpassfilter (För att få fram basbandet)
    # Vi vill ha kvar basbandet (ca 100 Hz bredd) men ta bort 2*fc (2000 Hz).
    # Vi sätter cutoff på 200 Hz för att vara säkra.
    cutoff_lp = 200 / nyquist
    b_lp, a_lp = signal.butter(4, cutoff_lp, btype='low')

    yI = signal.lfilter(b_lp, a_lp, yI_temp)
    yQ = signal.lfilter(b_lp, a_lp, yQ_temp)

    # D. Skapa komplex basbandssignal
    yb = yI + 1j * yQ

    # E. Avkodning (Decoding)
    # wcslib sköter synkroniseringen (hitta var signalen börjar) och fas-korrigering
    try:
        bits_rx = wcs.decode_baseband_signal(yb, Tb, fs)
        decoded_text = wcs.decode_string(bits_rx)
        
        print("\n================RESULTAT=================")
        print(f"Skickat meddelande: {message}")
        print(f"Mottaget meddelande: {decoded_text}")
        print(f"Antal bitar skickade: {len(bits_tx)}")
        print(f"Antal bitar mottagna: {len(bits_rx)}")
        
        if message == decoded_text:
            print("SUCCESS: Meddelandet överfördes korrekt!")
        else:
            print("FAIL: Det blev fel i överföringen.")
        print("=========================================\n")

    except Exception as e:
        print(f"Avkodning misslyckades: {e}")
        bits_rx = []

    # ==========================================
    # DEL 4: PLOTTA RESULTATET
    # ==========================================
    plt.figure(figsize=(12, 8))

    # 1. Mottagen signal (Innan demodulering)
    plt.subplot(3, 1, 1)
    plt.plot(t_rx[:1000], ym[:1000])
    plt.title("Mottagen signal (Filtrerad ym) - Zoom")
    plt.grid(True)

    # 2. Demodulerad Basbandssignal (Magnitud)
    plt.subplot(3, 1, 2)
    plt.plot(t_rx, np.abs(yb), 'g')
    plt.title("Demodulerad Basbandssignal (Magnitud |yb|)")
    plt.grid(True)
    
    # 3. Jämförelse I/Q (Fas)
    plt.subplot(3, 1, 3)
    plt.plot(t_rx, yI, label="I (In-phase)")
    plt.plot(t_rx, yQ, label="Q (Quadrature)", alpha=0.7)
    plt.title("I och Q Komponenter")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()