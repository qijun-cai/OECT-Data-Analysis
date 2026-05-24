# OECT Transient Behavior Plot
# Only curves, no response time calculation or axis adjustment function
# Latest update: 2026/05/24

# === Requirements ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# === Read CSV File ===
# CSV file template: OECT-transient.csv
data = pd.read_csv("OECT-transient.csv")

# === Extract Columns ===
# First column  -> Time (s)
# Second column -> Id (A)
time = data.iloc[:, 0]

# Take absolute value and convert A -> mA
Id = np.abs(data.iloc[:, 1]) * 1000

# === Figure Style ===
plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 12,
    "axes.labelsize": 12,
    "axes.titlesize": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "lines.linewidth": 2,
    "figure.dpi": 300,
})

# === Create Plot ===
fig, ax = plt.subplots(figsize=(4, 3))

ax.plot(time, Id,
        color="navy",
        linewidth=2)

# === Labels ===
ax.set_xlabel("Time (s)")
ax.set_ylabel("|Id| (mA)")

# === Tick style ===

# Major ticks
ax.tick_params(axis='both',
               which='major',
               direction='in',
               length=5,
               width=1.2)

# Minor ticks
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.yaxis.set_minor_locator(AutoMinorLocator(5))

ax.tick_params(axis='both',
               which='minor',
               direction='in',
               length=3,
               width=1)

# === Layout ===
plt.tight_layout()

# === Show Plot ===
plt.tight_layout()
plt.savefig("Preview-OECT_transient.png", dpi=600, bbox_inches="tight")
# plt.savefig("OECT_output_curves.pdf")

plt.show()
