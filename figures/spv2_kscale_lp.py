import numpy as np
from pathlib import Path
import penguins as pg
from penguins.private import nmrd
import matplotlib.pyplot as plt
plt.style.use(Path(__file__).parent / "helv.mplstyle")

path = nmrd() / "210310-7g-n15-sw1"
dss = [
    pg.read(path, 101001, 1),  # normal
    pg.read(path, 102001, 2),  # k = 2 +LP
    pg.read(path, 103001, 2),  # k = 4 +LP
    pg.read(path, 104001, 2),  # k = 8 +LP
    pg.read(path, 105001, 2),  # SW * 2 +LP
    pg.read(path, 106001, 2),  # SW * 4 +LP
    pg.read(path, 107001, 2),  # SW * 8 +LP
]
titles = [r"standard", r"(+LP) $k = 2$", r"(+LP) $k = 4$", r"(+LP) $k = 8$",
          r"(+LP) SW × 2", r"(+LP) SW × 4", r"(+LP) SW × 8"]

aqs = [f"{aq} ms" for aq in [60.1, 30.1, 15.0, 7.5, 30.1, 15.0, 7.5]]
aqeffs = [f"{aq} ms" for aq in [120.3] * 7]
sws = [f"{sw} ppm" for sw in [30, 30, 30, 30, 60, 120, 240]]
td1s = [256, 128, 64, 32, 256, 256, 256]
nss = [2, 4, 8, 16, 2, 2, 2]
noises = [1, 2, 4, 8, 2, 4, 8]

fig = plt.figure(figsize=(16, 12), constrained_layout=True)
gs = fig.add_gridspec(ncols=16, nrows=12)
axs = [
    fig.add_subplot(gs[2:6, 0:4]),
    fig.add_subplot(gs[0:4, 4:8]), fig.add_subplot(gs[0:4, 8:12]), fig.add_subplot(gs[0:4, 12:16]),
    fig.add_subplot(gs[4:8, 4:8]), fig.add_subplot(gs[4:8, 8:12]), fig.add_subplot(gs[4:8, 12:16]),
    fig.add_subplot(gs[9:11, 0:4]),
    fig.add_subplot(gs[8:10, 4:8]), fig.add_subplot(gs[8:10, 8:12]), fig.add_subplot(gs[8:10, 12:16]),
    fig.add_subplot(gs[10:12, 4:8]), fig.add_subplot(gs[10:12, 8:12]), fig.add_subplot(gs[10:12, 12:16])
]

f1b, f2b = "110..131", "7..9.3"

# Plot data.
for ds, ax, title, aq, aqeff, sw, td1, ns, noise in zip(dss, axs[:7], titles,
                                                        aqs, aqeffs, sws,
                                                        td1s, nss, noises):
    ds.stage(ax, levels=5e3*np.sqrt(noise), f1_bounds=f1b, f2_bounds=f2b)
    param_text = "\n".join([f"{param} = {value}" for param, value
                            in zip(["AQ", r"$\rm AQ_{eff}$", "SW", "TD1", "NS"],
                                   [aq, aqeff, sw, td1, ns])])
    ax.text(x=0.03, y=0.9, s=param_text, fontsize=12, transform=ax.transAxes,
            horizontalalignment="left", verticalalignment="top")
    pg.mkplot(ax, title=title, tight_layout=False)
    pg.ymove(ax, pos="topright", tight_layout=False)
for ds, ax, noise in zip(dss, axs[7:], noises):
    ds.f1projp().stage(ax, bounds=f1b, scale=1/np.sqrt(noise))
    pg.mkplot(ax, tight_layout=False)
# Standardise ylims of projections.
ymin, ymax = axs[10].get_ylim()
for ax in axs[7:]:
    ax.set_ylim(ymin, ymax*1.1)

# Calculate and display integrals
shifts = (113.23, 123.27, 125.43, 128.02)
margin = 0.2
get_integs = lambda ds: np.array([ds.f1projp().integrate(peak=shift,
                                                         margin=margin,
                                                         mode="max")
                                  for shift in shifts])
ref_integs = get_integs(dss[0])
for ds, ax, noise in zip(dss[1:], axs[8:], noises[1:]):
    integs = get_integs(ds)
    rel_integs = integs / (ref_integs * np.sqrt(noise))
    for shift, integ, rel_integ in zip(shifts, integs, rel_integs):
        voffset = (ymax*1.1 - ymin) * 0.05
        ax.text(x=shift, y=(integ/np.sqrt(noise))+voffset, s=f"{rel_integ:.1f}×",
                fontsize=9, horizontalalignment="center")


# Tidy up
pg.label_axes(axs[0:7], fstr="({})", fontweight="bold", fontsize=14)
pg.label_axes(axs[7:14], start=8, fstr="({})", fontweight="bold", fontsize=14,
              offset=(0.02, 0.05))

# Move the first Axes down a bit.
fig.execute_constrained_layout()    # This is needed not only for moving
                                    # the Axes, but also for pg.cleanup_axes().
                                    # Reasons unclear.
first_ax_bbox = axs[0].get_position()
first_ax_bbox.y0 = first_ax_bbox.y0 - 0.07
first_ax_bbox.y1 = first_ax_bbox.y1 - 0.07
axs[0].set_position(first_ax_bbox)

pg.cleanup_axes()
# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
