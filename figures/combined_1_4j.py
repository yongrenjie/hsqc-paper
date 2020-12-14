from pathlib import Path
import matplotlib.pyplot as plt
import penguins as pg
from penguins.private import nmrd
from penguins.private import Andrographolide as Andro
from penguins.private import hsqc_cosy_stripplot
plt.style.use(Path(__file__).parent / "helv.mplstyle")

path = nmrd() / "201115-7a-c13-sehsqc-full"

[sc_s, sc_c, crk_s,
 crk_c, sp_s, sp_c,
 edsc_s, edsc_c, edcrk_s,
 edcrk_c, edsp_s, edsp_c] = [pg.read(path, expno) for expno in
                             (11001, 11002, 13001, 13002, 17001, 17002,
                              12001, 12002, 14001, 14002, 18001, 18002)]

fig, axs = pg.subplots(2, 2)
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[crk_s, crk_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel=r"CRK seHSQC/CLIP-COSY ($\Delta' = 1/(4J)$)",
                    ylabel="intensity vs NOAH HSQC/CLIP-COSY",
                    ax=axs[0][0],
                    edited=False,
                    ncol=1, loc="upper right")
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[sp_s, sp_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel=r"NOAH seHSQC/CLIP-COSY ($\Delta' = 1/(4J)$)",
                    ylabel="intensity vs NOAH HSQC/CLIP-COSY",
                    ax=axs[0][1],
                    edited=False,
                    ncol=1, loc="upper right")
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[edcrk_s, edcrk_c],
                    ref_datasets=[edsc_s, edsc_c],
                    xlabel=r"CRK edited seHSQC/CLIP-COSY ($\Delta' = 1/(4J)$)",
                    ylabel="intensity vs NOAH edited HSQC/CLIP-COSY",
                    ax=axs[1][0],
                    edited=True,
                    ncol=1, loc="upper right")
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[edsp_s, edsp_c],
                    ref_datasets=[edsc_s, edsc_c],
                    xlabel=r"NOAH edited seHSQC/CLIP-COSY ($\Delta' = 1/(4J)$)",
                    ylabel="intensity vs NOAH edited HSQC/CLIP-COSY",
                    ax=axs[1][1],
                    edited=True,
                    ncol=1, loc="upper right")
pg.label_axes(axs, fontsize=14, fstr="({})", fontweight="bold")
axs[0][1].yaxis.set_visible(False)
axs[1][1].yaxis.set_visible(False)
for ax in axs.flat:
    ax.set_ylim(-0.3, 2.6)
    pg.style_axes(ax, "plot")

# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
