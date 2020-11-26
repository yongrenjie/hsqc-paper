from pathlib import Path
import penguins as pg
from penguins.private import nmrd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Source Sans Pro"

path = nmrd() / "200926-7z-n15-cnst16-scan"
path2 = nmrd() / "200926-7z-n15-sehsqc-full"

# seHSQC v2, cnst16 = 1, 2.5
dss = [pg.read(path, expno * 1000 + 1) for expno in (17, 32)]
# Standard seHSQC
dss = dss + [pg.read(path2, 8)] 
# Projections
projs = [ds.f2projp() for ds in dss]

titles = [
    "NOAH seHSQC, CTP gradient duration = 1.0 ms",
    "NOAH seHSQC, CTP gradient duration = 2.5 ms",
    "CRK seHSQC"
]

fig, axs = pg.subplots(2, 3, figsize=(12, 6),
                       gridspec_kw={"height_ratios": [3, 1]})

# Plot 2Ds
for ds, ax, title in zip(dss, axs[0], titles):
    ds.stage(ax, levels=5e3, f1_bounds="85..135", f2_bounds="1.5..11.5")
    pg.mkplot(ax, title=title)
# Plot projections onto f2 axis
for proj, ax in zip(projs, axs[1]):
    proj.stage(ax, bounds="1.5..11.5")
    pg.mkplot(ax)
# Scale projections to be the same
ymin, ymax = axs[1][2].get_ylim()
for ax in axs[1]:
    ax.set_ylim((ymin, ymax))
# Indicate relative integrals.
peaks = (2.23, 7.78, 10.70)
ref_int = projs[0].integrate(peak=10.7, margin=0.5, mode="max")
for proj, ax in zip(projs, axs[1]):
    for peak in peaks:
        integ = proj.integrate(peak=peak, margin=0.5, mode="max")
        rel_int = integ / ref_int
        ax.text(x=peak, y=integ+1e3, s=f"{rel_int:.2f}×",
                horizontalalignment="left", verticalalignment="bottom")


pg.label_axes(axs, fstr="({})", fontweight="bold", fontsize=16)

# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype), dpi=500)
