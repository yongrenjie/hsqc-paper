from pathlib import Path
from itertools import product
import penguins as pg
from penguins.private import nmrd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
plt.style.use(Path(__file__).parent / "helv.mplstyle")

path = nmrd() / "201205-7a-noah-examples"
dss = [pg.read(path, expno) for expno in range(4001, 4005)]

hb = (0.3, 7)
cb = (10, 152)
fig, axs = pg.subplots(2, 2)
dss[0].stage(axs.flat[0], levels=7e3, colors=("blue", "white"),
             f1_bounds=cb, f2_bounds=hb)
dss[1].stage(axs.flat[1], levels=1e4,
             f1_bounds=cb, f2_bounds=hb)
dss[2].stage(axs.flat[2], levels=3e5, colors=("blue", "white"),
             f1_bounds=hb, f2_bounds=hb)
dss[3].stage(axs.flat[3], levels=4e4, colors=("blue", "white"),
             f1_bounds=hb, f2_bounds=hb)
pg.mkplots()
for ax in axs.flat:
    pg.move_ylabel(ax, "topright")

# Add labels
pg.label_axes(axs, fstr="({})", fontweight="semibold", fontsize=14)

pg.cleanup_axes()
# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
