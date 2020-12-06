from itertools import product
from pathlib import Path
import numpy as np
import penguins as pg
import matplotlib.pyplot as plt
from penguins.private import nmrd

path = nmrd() / "201017-7g-n15-sehsqc-full"
plt.rcParams["font.family"] = "Source Sans Pro"

spv2 = pg.read(path, 42001)
m = pg.read(path, 12001)
f1_bounds = (112.2, 128.9)
f2_bounds = (7.0, 9.3)

fig, axs = pg.subplots(2, 2, figsize=(6, 4),
                       gridspec_kw={'height_ratios': [3, 1]})
# Plot 2Ds
m.stage(ax=axs[0][0], levels=(5e3, 1.2, 20),
        f1_bounds=f1_bounds, f2_bounds=f2_bounds)
spv2.stage(ax=axs[0][1], levels=(5e3, 1.2, 20),
           f1_bounds=f1_bounds, f2_bounds=f2_bounds)
for ax in axs[0]:
    pg.move_ylabel(ax, "topright")

# Plot projections
f1_bounds=(112.2, 132)  # to avoid collision with label
m.f1projp().stage(ax=axs[1][0], bounds=f1_bounds)
spv2.f1projp().stage(ax=axs[1][1], bounds=f1_bounds)
pg.mkplots()

# Calculate integrals and add text on Spv2 projection
shifts = (113.23, 123.27, 125.43, 128.02)
margin = 0.2
spv2_ints = np.array([spv2.f1projp().integrate(peak=shift,
                                               margin=margin,
                                               mode="max")
                      for shift in shifts])
m_ints = np.array([m.f1projp().integrate(peak=shift,
                                         margin=margin,
                                         mode="max")
                   for shift in shifts])
rel_ints = spv2_ints / m_ints
for shift, spv2_int, rel_int in zip(shifts, spv2_ints, rel_ints):
    voffset = 5e3 if shift == 123.27 else 3e3  # avoid collision
    axs[1][1].text(x=shift, y=spv2_int+voffset, s=f"{rel_int:.1f}×",
                   fontsize=9, horizontalalignment="center")
ymin, ymax = axs[1][1].get_ylim()
for ax in axs[1]:
    ax.set_ylim((ymin, ymax*1.2))

# Label axes
pg.label_axes(axs, fstr="({})", fontsize=16, fontweight="bold")

pg.cleanup_axes()
# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype), dpi=500)
