import numpy as np
from pathlib import Path
import penguins as pg
from penguins.private import nmrd
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Source Sans Pro"
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.it"] = "Source Sans Pro:italic"

path = nmrd() / "201017-7g-n15-sehsqc-full"
ks = [1, 2, 4, 8]
expnos = [12001, 13001, 14001, 15001]
dss = [pg.read(path, expno) for expno in expnos]

#######################################################################
# If we change to 2x4 then only this block of code needs to be modified.
#######################################################################
fig, axs = pg.subplots(2, 4, figsize=(16, 6),
                       gridspec_kw={"height_ratios": [2, 1]})
# Make these flat lists of the relevant axes, and the rest of the code will
# work.
axes_2d = axs[0]
axes_1d = axs[1]
#######################################################################

# Plot 2Ds
for ds, ax, k in zip(dss, axes_2d, ks):
    ds.stage(ax, levels=5e3, f1_bounds="110..130", f2_bounds="7..9.3")
    pg.mkplot(ax, title=f"HMQC, $k$ = {k}")

# Plot 1D projections
for ds, ax, k in zip(dss, axes_1d, ks):
    ds.f1projp().stage(ax, bounds="110..132")
    pg.mkplot(ax)
# Set ylims to be the same
ymin, ymax = axes_1d[3].get_ylim()
for ax in axes_1d:
    ax.set_ylim((ymin, ymax))
# Calculate and display integrals
shifts = (113.23, 123.27, 125.43, 128.02)
margin = 0.2
ref_ints = np.array([dss[0].f1projp().integrate(peak=shift, margin=margin, mode="max")
                      for shift in shifts])
for ds, ax in zip(dss[1:], axes_1d[1:]):
    abs_ints = np.array([ds.f1projp().integrate(peak=shift, margin=margin, mode="max")
                         for shift in shifts])
    rel_ints = abs_ints / ref_ints
    for shift, abs_integ, rel_integ in zip(shifts, abs_ints, rel_ints):
        voffset = 2e3
        ax.text(x=shift, y=abs_integ+voffset, s=f"{rel_integ:.1f}×",
                fontsize=9, horizontalalignment="center")

pg.label_axes(axs, fstr="({})", fontweight="bold", fontsize=16)
# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype), dpi=500)
