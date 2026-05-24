# OECT Output Curves
# Latest update: 2026/05/24
# Note: Template named "OECT-output.csv" is highly recommended to be used.

# === Requirements ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# === Figure Style ===
plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 12,
    "axes.labelsize": 12,
    "axes.titlesize": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "lines.linewidth": 1,
    "figure.dpi": 300,
})

# === Import Data ===
df = pd.read_csv("OECT-output.csv")
# print(df.columns) # for debug

# First column = Vd
Vd = df["Vd"].to_numpy()

# Remaining columns = Id under different Vg
# Example columns: Vg0, Vg-0.2, Vg-0.4 ...
gate_columns = df.columns[1:]

# === Plot ===
fig, ax = plt.subplots(figsize=(4, 3))

for col in gate_columns:
    Id = df[col].to_numpy()
    Id_mA = np.abs(Id) * 1000   # Convert A → mA
    
    ax.plot(Vd, Id_mA, label=col)

# === Axis Format ===
ax.set_xlabel("Vd (V)")
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

# === Legend ===
ax.legend(frameon=False, loc="best", ncol=1)

# === Title ===
# ax.set_title("OECT Output Curves")

# === Save ===
plt.tight_layout()
plt.savefig("OECT_output_curves.png", dpi=600, bbox_inches="tight")
# plt.savefig("OECT_output_curves.pdf")

plt.show()
