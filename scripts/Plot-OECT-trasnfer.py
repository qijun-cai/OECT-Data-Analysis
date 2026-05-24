# OECT Transfer Curve
# Latest update: 2026/05/24

# === Requirements ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Define y-axis scale ===
scale_type = input(
    "Choose y-axis scale for |Id| (linear/log): "
).strip().lower()

if scale_type not in ["linear", "log"]:
    print("Invalid input. Defaulting to linear.")
    scale_type = "linear"
# Ask |Id| axis range (on left)
set_id_range = input(
    "Set |Id| y-axis range? (y/n): "
).strip().lower()

# Ask gm axis range (on right)
set_gm_range = input(
    "Set gm y-axis range? (y/n): "
).strip().lower()

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

# === Import Data ===
df = pd.read_csv("OECT-tf.csv") # paste your data into this table in advance

Vg = df["Vg"].to_numpy()        # Gate voltage (V)
Id = df["Id"].to_numpy()        # Drain current (A)

# === Data Processing ===
Id_mA = np.abs(Id) * 1000       # Convert A → mA, absolute value

gm = np.gradient(Id, Vg)        # Transconductance (S)
gm_mS = gm * 1000               # Convert S → mS

# === Export processed data in CSV with Vg, Id, gm ===
output_df = pd.DataFrame({
    "Vg (V)": Vg,
    "Id (A)": Id,
    "|Id| (mA)": Id_mA,
    "gm (S)": gm,
    "gm (mS)": gm_mS
})

output_df.to_csv("processed_OECT_tf.csv", index=False)

# === Plot ===
fig, ax1 = plt.subplots(figsize=(4, 3))

# Left axis: |Id|
line1 = ax1.plot(
    Vg,
    Id_mA,
    label='|Id|',
    color='black'
)

ax1.tick_params(direction='in')
ax1.set_xlabel("Vg (V)")
ax1.set_ylabel("|Id| (mA)")
ax1.spines['top'].set_visible(True)

# Set y-axis scale
ax1.set_yscale(scale_type)
# Set Id axis range
if set_id_range == "y":

    id_min = float(input("Enter |Id| ymin (mA): "))
    id_max = float(input("Enter |Id| ymax (mA): "))

    ax1.set_ylim(id_min, id_max)

# Right axis: gm
ax2 = ax1.twinx()
ax2.tick_params(direction='in')
line2 = ax2.plot(
    Vg,
    gm_mS,
    '--',
    label='gm',
    color='red'
)

ax2.set_ylabel("gm (mS)")
ax2.spines['top'].set_visible(False)

# Set gm axis range
if set_gm_range == "y":

    gm_min = float(input("Enter gm ymin (mS): "))
    gm_max = float(input("Enter gm ymax (mS): "))

    ax2.set_ylim(gm_min, gm_max)

# === Combine Legend ===
lines = line1 + line2
labels = [l.get_label() for l in lines]

ax1.legend(
    lines,
    labels,
    frameon=False,
    loc="best"
)

# === Save & Display Figure ===
plt.tight_layout()

plt.savefig(
    f"OECT_transfer_{scale_type}.png",
    dpi=600,
    bbox_inches="tight"
)

# plt.savefig(f"OECT_transfer_curve_{scale_type}.pdf")

plt.show()
