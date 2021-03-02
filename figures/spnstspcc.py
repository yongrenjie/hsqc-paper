from pathlib import Path
from itertools import product
import penguins as pg
from penguins.private import nmrd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
plt.style.use(Path(__file__).parent / "helv.mplstyle")

path = nmrd() / "201119-7g-noah-xspstspx"
dss = [pg.read(path, expno) for expno in range(15001, 15005)]

fig, axs = pg.subplots2d(2, 2, figsize=(6, 5.6))
dss[0].stage(axs.flat[0], levels=7e3,
             f1_bounds="112..129", f2_bounds="7..9.3")
dss[1].stage(axs.flat[1], levels=4e3, colors=("blue", "white"),
             f1_bounds="12..68", f2_bounds="0.5..5.2")
dss[2].stage(axs.flat[2], levels=8e3,
             f1_bounds="12..68", f2_bounds="0.5..5.2")
# dss[3].stage(axs.flat[3], levels=7e4, colors=("blue", "white"),
#              f1_bounds="0.2..10", f2_bounds="0.2..10")
dss[3].stage(axs.flat[3], levels=3e5, colors=("blue", "white"),
             f1_bounds="0.5..5.2", f2_bounds="0.5..5.2")
pg.mkplots()
for ax in axs.flat:
    pg.move_ylabel(ax, "topright", dx=0.02)

# Add labels
pg.label_axes(axs, fstr="({})", fontweight="semibold", fontsize=14)

pg.cleanup_axes()
# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
