# OECT Transient Response Time Analysis
# Latest update: 2026/05/24
# 1. This script includes calculating on- and off- repsonse time values
#    and plotting fitted curves on the original transient cuvrse.
# 2. The time range (x-axis) can also be set manually.

# =====================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.ticker import AutoMinorLocator

# =====================================
# Read CSV File
# =====================================

# CSV file name
data = pd.read_csv("OECT-transient.csv")

# First column = Time(s)
time = data.iloc[:, 0].values

# Second column = Id(A)
# Convert to absolute value and mA
Id = np.abs(data.iloc[:, 1].values) * 1000

# =====================================
# Input transient regions from terminal
# =====================================

print("=== Input ON transient region ===")
on_start = float(input("ON start time (s): "))
on_end   = float(input("ON end time (s): "))

print("\n=== Input OFF transient region ===")
off_start = float(input("OFF start time (s): "))
off_end   = float(input("OFF end time (s): "))

# Create masks
mask_on = (time >= on_start) & (time <= on_end)
mask_off = (time >= off_start) & (time <= off_end)

# =====================================
# Input axis display range
# =====================================

print("\n=== Input X-axis display range ===")
x_min = float(input("X-axis minimum: "))
x_max = float(input("X-axis maximum: "))

print("\n=== Input Y-axis display range ===")
y_min = float(input("Y-axis minimum: "))
y_max = float(input("Y-axis maximum: "))

# =====================================
# Extract data
# =====================================

# Raw time axis (for plotting)
t_on_raw = time[mask_on]
t_off_raw = time[mask_off]

# Current data
I_on = Id[mask_on]
I_off = Id[mask_off]

# Reset time axis to start from 0 (required for exponential fitting)
t_on = t_on_raw - t_on_raw[0]
t_off = t_off_raw - t_off_raw[0]

# =====================================
# Define exponential functions
# =====================================

# ON transient
def on_func(t, I_inf, I0, tau):
    return I_inf - (I_inf - I0) * np.exp(-t / tau)

# OFF transient
def off_func(t, I0, I_inf, tau):
    return I0 + (I_inf - I0) * np.exp(-t / tau)

# =====================================
# Initial guess for fitting
# =====================================

p0_on = [I_on[-1], I_on[0], 0.1]
p0_off = [I_off[-1], I_off[0], 0.1]

# =====================================
# Curve fitting
# =====================================

# ON fit
params_on, _ = curve_fit(on_func, t_on, I_on, p0=p0_on)
Iinf_on, I0_on, tau_on = params_on

# OFF fit
params_off, _ = curve_fit(off_func, t_off, I_off, p0=p0_off)
I0_off, Iinf_off, tau_off = params_off

# =====================================
# Generate fitted curves
# =====================================

fit_on = on_func(t_on, *params_on)
fit_off = off_func(t_off, *params_off)

# =====================================
# Figure style
# =====================================

plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 12,
    "axes.linewidth": 1.5
})

# =====================================
# Plot
# =====================================

fig, ax = plt.subplots(figsize=(7, 4.5))

# Experimental data
ax.plot(time, Id,
        color='navy',
        linewidth=2.5,
        label='Id')

# ON fitting
ax.plot(t_on_raw, fit_on,
        '--',
        color='red',
        linewidth=2,
        label=f'τON = {tau_on:.3f} s')

# OFF fitting
ax.plot(t_off_raw, fit_off,
        '--',
        color='green',
        linewidth=2,
        label=f'τOFF = {tau_off:.3f} s')

# =====================================
# Labels
# =====================================

ax.set_xlabel("Time (s)")
ax.set_ylabel("|Id| (mA)")

# =====================================
# Axis limits
# =====================================

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# =====================================
# Tick style
# =====================================

# Major ticks
ax.tick_params(axis='both',
               which='major',
               direction='in',
               length=5,
               width=1.2)

# Minor ticks
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())

ax.tick_params(axis='both',
               which='minor',
               direction='in',
               length=3,
               width=1)

# =====================================
# Legend
# =====================================

ax.legend(frameon=True)

# =====================================
# Layout and save
# =====================================

plt.tight_layout()

plt.savefig(
    "OECT_transient_tau.png",
    dpi=600,
    bbox_inches="tight"
)

# plt.savefig("OECT_transient_tau.pdf") 

plt.show()

# =====================================
# Print response times
# =====================================
print(f"\nON response time τ_on  = {tau_on:.4f*1000} ms")
print(f"OFF response time τ_off = {tau_off:.4f*1000} ms")
