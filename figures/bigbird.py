from pathlib import Path
import matplotlib.pyplot as plt
import penguins as pg
from penguins.private import nmrd
from penguins.private import Andrographolide as Andro
from penguins.private import hsqc_cosy_stripplot

path = nmrd() / "201115-7a-c13-sehsqc-full"
plt.rcParams["font.family"] = "Source Sans Pro"

[sc_s, sc_c, bb_s,
 bb_c, sp_s, sp_c,
 edsc_s, edsc_c, edbb_s,
 edbb_c, edsp_s, edsp_c] = [pg.read(path, expno) for expno in
                            (11001, 11002, 29001, 29002, 23001, 23002,
                             12001, 12002, 30001, 30002, 24001, 24002)]

fig, axs = pg.subplots(2, 2)
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[bb_s, bb_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel=r"NOAH seHSQC with BIG-BIRD/CLIP-COSY",
                    ylabel="intensity vs NOAH HSQC/CLIP-COSY",
                    ax=axs[0][0],
                    edited=False,
                    ncol=1, loc="upper right")
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[sp_s, sp_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel=r"NOAH seHSQC with ISR/CLIP-COSY",
                    ylabel="intensity vs NOAH HSQC/CLIP-COSY",
                    ax=axs[0][1],
                    edited=False,
                    ncol=1, loc="upper right")
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[edbb_s, edbb_c],
                    ref_datasets=[edsc_s, edsc_c],
                    xlabel=r"NOAH edited seHSQC with BIG-BIRD/CLIP-COSY",
                    ylabel="intensity vs NOAH edited HSQC/CLIP-COSY",
                    ax=axs[1][0],
                    edited=True,
                    ncol=1, loc="upper right")
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[edsp_s, edsp_c],
                    ref_datasets=[edsc_s, edsc_c],
                    xlabel=r"NOAH edited seHSQC with ISR/CLIP-COSY",
                    ylabel="intensity vs NOAH edited HSQC/CLIP-COSY",
                    ax=axs[1][1],
                    edited=True,
                    ncol=1, loc="upper right")
pg.label_axes(axs, fontsize=16, fstr="({})", fontweight="bold")
axs[0][1].yaxis.set_visible(False)
axs[1][1].yaxis.set_visible(False)
for ax in axs.flat:
    ax.set_ylim(0.4, 2)
    pg.style_axes(ax, "plot")

# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype), dpi=500)
