from pathlib import Path
import penguins as pg
from penguins.private import nmrd
import matplotlib.pyplot as plt
plt.style.use(Path(__file__).parent / "helv.mplstyle")

path = nmrd() / "200926-7z-n15-cnst16-scan"
path2 = nmrd() / "200926-7z-n15-sehsqc-full"

# seHSQC v2, cnst16 = 1, 2.5
dss = [pg.read(path, expno * 1000 + 1) for expno in (17, 32)]
# Standard seHSQC
dss = dss + [pg.read(path2, 8)] 
# Projections
projs = [ds.f2projp() for ds in dss]

titles = [
    "NOAH seHSQC, 1.0 ms gradients",
    "NOAH seHSQC, 2.5 ms gradients",
    "CRK seHSQC"
]

fig, axs = pg.subplots2d(3, 3, figsize=(12, 7),
                       gridspec_kw={"height_ratios": [0.5, 3, 1]})

# Plot 1D proton
proton = pg.read(path2, 1)
for ax, title in zip(axs[0], titles):
    proton.stage(ax=ax, color="blue")
    pg.mkplot(ax, title=title)
    ax.set(xlim=(11.5, 1.5))
    ax.xaxis.set_visible(False)
    ax.spines["bottom"].set_visible(False)

# Plot 2Ds
for ds, ax in zip(dss, axs[1]):
    ds.stage(ax, levels=5e3, f1_bounds="85..135", f2_bounds="1.5..11.5")
    pg.mkplot(ax)
# Plot projections onto f2 axis
for proj, ax in zip(projs, axs[2]):
    proj.stage(ax, bounds="1.5..11.5")
    pg.mkplot(ax)
# Scale projections to be the same
ymin, ymax = axs[2][2].get_ylim()
for ax in axs[2]:
    ax.set_ylim((ymin, ymax))
# Indicate relative integrals.
peaks = (2.23, 7.78, 10.70)
ref_int = projs[0].integrate(peak=10.7, margin=0.5, mode="max")
for proj, ax in zip(projs, axs[2]):
    for peak in peaks:
        integ = proj.integrate(peak=peak, margin=0.5, mode="max")
        rel_int = integ / ref_int
        ax.text(x=peak, y=integ+1e3, s=f"{rel_int:.2f}×",
                horizontalalignment="left", verticalalignment="bottom")

for ax in axs[1]:
    pg.move_ylabel(ax, pos="topright")
pg.label_axes(axs[1:], fstr="({})", fontweight="bold", fontsize=14)
pg.cleanup_axes()

for ax in axs[0]:
    # move them downwards
    x0, y0, w, h = ax.get_position().bounds
    ax.set_position([x0, y0-0.1, w, h])

# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype),
               bbox_inches="tight")
