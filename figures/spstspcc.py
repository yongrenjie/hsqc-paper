from pathlib import Path
from itertools import product
import penguins as pg
from penguins.private import nmrd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs

plt.rcParams["font.family"] = "Source Sans Pro"

path = nmrd() / "201119-7g-noah-xspstspx"
dss = [pg.read(path, expno) for expno in range(15001, 15005)]

fig, axs = pg.subplots(2, 2, figsize=(6, 6))
dss[0].stage(axs.flat[0], levels=7e3, f1_bounds="112..129", f2_bounds="7..9.3")
dss[1].stage(axs.flat[1], levels=3e3, colors=("blue", "white"),
             f1_bounds="12..134", f2_bounds="0.2..9.6")
dss[2].stage(axs.flat[2], levels=8e3, f1_bounds="12..134", f2_bounds="0.2..9.6")
dss[3].stage(axs.flat[3], levels=6e4, colors=("blue", "white"),
             f1_bounds="0.2..9.6", f2_bounds="0.2..9.6")
pg.mkplots()

###############
## TEMPORARY ##
###############
from matplotlib.patches import Rectangle as R
axs.flat[1].add_patch(R(xy=(0.4, 14), width=9, height=52, color="red", fill=False))
axs.flat[2].add_patch(R(xy=(0.4, 14), width=9, height=52, color="red", fill=False))
axs.flat[1].add_patch(R(xy=(0.5, 15), width=4.5, height=50, color="green", fill=False))
axs.flat[2].add_patch(R(xy=(0.5, 15), width=4.5, height=50, color="green", fill=False))

# Add labels
xs, ys = (0.02, 0.52), (0.98, 0.49)
yxs = product(ys, xs)
for yx, c in zip(yxs, "abcd"):
    fig.text(x=yx[1], y=yx[0], s=f"({c})", size=16, fontweight="bold",
             horizontalalignment="left", verticalalignment="top")
plt.subplots_adjust(left=0.15, wspace=0.37)

# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype), dpi=500)
