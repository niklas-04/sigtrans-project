# parameters.py - Inställningar för Grupp 5
import numpy as np

# --- Samplingsinställningar ---
# Vi väljer 48000 Hz. Det är standard för ljudkort och
# en multipel av er bärvåg (48 * 1000 Hz), vilket krävs i Lab 2.
fs = 48000
dt = 1/fs

# --- Grupp 5 Specifika Parametrar ---
# Kanal 1: 900 Hz - 1100 Hz
fc = 1000           # Bärvågsfrekvens (mitten av bandet)
Wc = 2 * np.pi * fc # Vinkelhastighet

# Effektbegränsning: 30 dBm = 1 Watt
# P = A^2 / 2  =>  1 = A^2 / 2  =>  A = sqrt(2)
Ac = np.sqrt(2) 

# --- Symboltid ---
# Vi väljer 10 perioder per symbol.
# Tc = 1ms. Tb = 10ms.
# Detta ger en smal signal som ryms i 200 Hz bandbredd.
Tb = 0.010