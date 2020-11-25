import penguins as pg
from penguins.private import Andrographolide as Andro
from penguins.private import nmrd, hsqc_cosy_stripplot
from pathlib import Path
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Source Sans Pro"
plt.rcParams["legend.labelspacing"] = 0.2
plt.rcParams["legend.handlelength"] = 0.5

p = nmrd() / "201115-7a-c13-sehsqc-full"
sc_s = pg.read(p, 11001)
sc_c = pg.read(p, 11002)
sporc_s = pg.read(p, 19001)
sporc_c = pg.read(p, 19002)
spv2c_s = pg.read(p, 23001)
spv2c_c = pg.read(p, 23002)
fig, axs = pg.subplots(1, 2, figsize=(6, 3.5))
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[sporc_s, sporc_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel="CRK seHSQC/CLIP-COSY",
                    ylabel="intensity vs NOAH HSQC/CLIP-COSY",
                    ax=axs[0],
                    ncol=1, loc="upper right", size=4)
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[spv2c_s, spv2c_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel="NOAH seHSQC/CLIP-COSY",
                    ylabel="intensity vs NOAH HSQC/CLIP-COSY",
                    ax=axs[1],
                    ncol=1, loc="upper right", size=4)

pg.label_axes(axs, fstr="({})", fontsize=16, fontweight="bold")
axs[1].yaxis.set_visible(False)
for ax in axs:
    ax.set_ylim(-0.2, 2.4)
    pg.style_axes(ax, "plot")

# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype), dpi=500)
