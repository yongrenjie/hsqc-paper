from pathlib import Path
import matplotlib.pyplot as plt
import penguins as pg
from penguins.private import nmrd
from penguins.private import Andrographolide as Andro
from penguins.private import hsqc_cosy_stripplot
plt.style.use(Path(__file__).parent / "helv.mplstyle")

path = nmrd() / "201115-7a-c13-sehsqc-full"

[sc_s, sc_c, crk_s, crk_c, sp_s, sp_c] = [pg.read(path, expno) for expno in
                                          (12001, 12002, 20001,
                                           20002, 24001, 24002)
                                          ]

fig, axs = pg.subplots(1, 2)
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[crk_s, crk_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel="CRK edited seHSQC/CLIP-COSY",
                    ylabel="intensity vs NOAH edited HSQC/CLIP-COSY",
                    ax=axs[0],
                    edited=True,
                    ncol=1, loc="upper right")
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[sp_s, sp_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel="NOAH edited seHSQC/CLIP-COSY",
                    ylabel="intensity vs NOAH edited HSQC/CLIP-COSY",
                    ax=axs[1],
                    edited=True,
                    ncol=1, loc="upper right")
pg.label_axes(axs, fontsize=14, fstr="({})", fontweight="bold")
axs[1].yaxis.set_visible(False)
for ax in axs:
    ax.set_ylim(-0.3, 2.1)
    pg.style_axes(ax, "plot")

# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
