from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import penguins as pg
from penguins.private import nmrd
plt.style.use(Path(__file__).parent / "helv.mplstyle")

path = nmrd() / "201115-7a-sehsqc-grads"
dss = [pg.read(path, expno) for expno in (1002, 5002, 6002, 7002)]
slices = [ds.slice(axis=0, ppm=0.667) for ds in dss]

fig, axs = pg.subplots2d(1, 2, figsize=(9, 4),
                       gridspec_kw={"width_ratios": [4, 6]})

# Sample 2D
dss[3].stage(ax=axs[0], levels=2e5, f1_bounds="0..7.5", f2_bounds="0..7.5")
pg.mkplot(axs[0])
pg.ymove(axs[0], "topright")
axs[0].add_patch(Rectangle((0.45, 0.05), 0.42, 1.22,
                           fill=False, color="grey", linestyle="--"))

# 1Ds
peak_centre = 0.667
plot_margin = 0.6
labels = ["(on, on)", "(on, off)",
          "(off, on)", "(off, off)"]
for s, l in zip(slices, labels):
    s.stage(axs[1],
            bounds=(peak_centre - plot_margin, peak_centre + plot_margin),
            label=l)
pg.mkplot(axs[1], hoffset=2.2*plot_margin)
axs[1].xaxis.set_visible(False)
axs[1].legend(ncol=2, loc="upper center")
pg.style_axes(axs[1], "2d")

pg.cleanup_axes()
pg.label_axes(axs, fstr="({})", fontsize=14, fontweight="bold")

# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
