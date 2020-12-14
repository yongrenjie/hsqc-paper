from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow
import penguins as pg
from penguins.private import nmrd
plt.style.use(Path(__file__).parent / "helv.mplstyle")

path = nmrd() / "201017-7g-n15-sehsqc-full"
expnos = [42003, 105003, 106003, 107003]
dss = [pg.read(path, expno) for expno in expnos]

fig, axs = pg.subplots(2, 2)
for ds, ax in zip(dss, axs.flat):
    ds.stage(ax=ax, levels=3e4)

titles = [
    "extra gradient in both seHSQCs",
    r"extra gradient in only $^{15}$N seHSQC",
    r"extra gradient in only $^{13}$C seHSQC",
    "no extra gradients"
]
pg.mkplots(axs, titles)
pg.label_axes(axs, fstr="({})", fontsize=14, fontweight="bold")
for ax in axs.flat:
    pg.move_ylabel(ax, pos="topright")
pg.cleanup_axes()

# Add arrows pointing to the artefacts
def highlight_15n_artefacts(ax):
    line_kwargs = {"color": "C1", "linewidth": 1.2,
                   "linestyle": "--", "zorder": -5, "alpha": 0.6}
    ax.plot([9.08, 0.79], [1.02, 9.09], **line_kwargs)
    ax.plot([2.96, 0.79], [11.01, 4.61], **line_kwargs)
    ax.plot([2.96, 7.04], [-1.01, 11.01], **line_kwargs)
    ax.plot([7.04, 9.08], [-1.01, 5.16], **line_kwargs)
    dx = 0.7
    dy = -0.7
    width = 0.3
    color = "C1"
    ax.add_patch(Arrow(x=0.5-dx, y=4.62-dy, dx=dx, dy=dy, width=width,
                       color=color, transform=ax.transData))
    ax.add_patch(Arrow(x=0.5-dx, y=9.10-dy, dx=dx, dy=dy, width=width,
                       color=color, transform=ax.transData))
    ax.add_patch(Arrow(x=3.6+dx, y=0.2+dy, dx=-dx, dy=-dy, width=width,
                       color=color, transform=ax.transData))
def highlight_13c_artefacts(ax):
    line_kwargs = {"color": "C2", "linewidth": 1.2,
                   "linestyle": "--", "zorder": -5, "alpha": 0.6}
    ax.plot([9.08, 0.79], [8.37, 1.54], **line_kwargs)
    ax.plot([9.08, 0.79], [9.83, 0.05], **line_kwargs)
    dx = +0.7
    dy = -0.7
    width = 0.3
    color = "C2"
    ax.add_patch(Arrow(x=0.5-dx, y=0.0-dy, dx=dx, dy=dy, width=width,
                       color=color, transform=ax.transData))
    ax.add_patch(Arrow(x=0.5-dx, y=1.6-dy, dx=dx, dy=dy, width=width,
                       color=color, transform=ax.transData))
    ax.add_patch(Arrow(x=9.3+dx, y=8.3+dy, dx=-dx, dy=-dy, width=width,
                       color=color, transform=ax.transData))
    ax.add_patch(Arrow(x=9.3+dx, y=9.7+dy, dx=-dx, dy=-dy, width=width,
                       color=color, transform=ax.transData))
highlight_13c_artefacts(axs[0][1])
highlight_15n_artefacts(axs[1][0])
highlight_15n_artefacts(axs[1][1])
highlight_13c_artefacts(axs[1][1])

# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
