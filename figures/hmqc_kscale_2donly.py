import numpy as np
from pathlib import Path
import penguins as pg
from penguins.private import nmrd
from penguins.private import Gramicidin as Grami
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Source Sans Pro"
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.it"] = "Source Sans Pro:italic"

path = nmrd() / "201017-7g-n15-sehsqc-full"
ks = [1, 2, 4, 8]
expnos = [12001, 13001, 14001, 15001]
dss = [pg.read(path, expno) for expno in expnos]

fig, axs = pg.subplots(2, 2)

# Plot 2Ds
for ds, ax, k in zip(dss, axs.flat, ks):
    ds.stage(ax, levels=5e3, f1_bounds="110..130", f2_bounds="7..9.3")
    pg.mkplot(ax, title=f"HMQC, $k$ = {k}")

# Calculate and display integrals
peaks = Grami.nhsqc_peaks
margin = Grami.nhsqc.margin
ref_ints = np.array([dss[0].integrate(peak=peak, margin=margin, mode="max")
                      for peak in peaks])
for ds, ax in zip(dss[1:], axs.flat[1:]):
    abs_ints = np.array([ds.integrate(peak=peak, margin=margin, mode="max")
                         for peak in peaks])
    rel_ints = abs_ints / ref_ints
    for peak, abs_integ, rel_integ in zip(peaks, abs_ints, rel_ints):
        voffset = 2e3
        ax.text(x=peak[1], y=peak[0]-1.5, s=f"({rel_integ:.1f}×)",
                fontsize=9, horizontalalignment="center",
                transform=ax.transData)

pg.label_axes(axs, fstr="({})", fontweight="bold", fontsize=16)
# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype), dpi=500)
