from pathlib import Path
from itertools import product
import penguins as pg
from penguins.private import nmrd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
plt.style.use(Path(__file__).parent / "helv.mplstyle")

path = nmrd() / "201120-7z-noah-xspstspx"
dss = [pg.read(path, expno, procno)
       for expno, procno in [(10001, 1), (10002, 2), (10003, 1), (10004, 1)]]

fig, axs = pg.subplots2d(2, 2)
dss[0].stage(axs.flat[0], levels=7e3, colors=("blue", "white"),
             f1_bounds=(20, 165), f2_bounds=(1.8, 11.5))
dss[1].stage(axs.flat[1], levels=3e4,
             f1_bounds=(86, 133), f2_bounds=(7.4, 11.3))
dss[2].stage(axs.flat[2], levels=2e4,
             f1_bounds=(20, 128), f2_bounds=(1.8, 7.7))
dss[3].stage(axs.flat[3], levels=5e5, colors=("blue", "white"),
             f1_bounds=(1.8, 7.7), f2_bounds=(1.8, 7.7))
pg.mkplots()
for ax in axs.flat:
    pg.move_ylabel(ax, "topright")

# Add labels
pg.label_axes(axs, fstr="({})", fontweight="semibold", fontsize=14)

pg.cleanup_axes()
# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
