from scipy import signal
from parameters import dt

def design_lowpass_filter():
    fs = 1 / dt
    N = 4  # filter order

    cutoff = 40  # Hz (optimal for Tb = 0.025)

    b, a = signal.butter(
        N,
        cutoff,
        btype="lowpass",
        fs=fs,
        output="ba"
    )
    return b, a

b_lp, a_lp = design_lowpass_filter()
print("Low-pass filter coefficients:")
print("b:", b_lp)
print("a:", a_lp)