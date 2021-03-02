from pathlib import Path
import matplotlib.pyplot as plt
import penguins as pg
from penguins.private import nmrd
from penguins.private import Andrographolide as Andro
from penguins.private import hsqc_cosy_stripplot
plt.style.use(Path(__file__).parent / "helv.mplstyle")

path = nmrd() / "201115-7a-c13-sehsqc-full"

[sc_s, sc_c,
 crk_s, crk_c,
 spv1_s, spv1_c,
 spv2_s, spv2_c,
 edsc_s, edsc_c,
 edcrk_s, edcrk_c,
 edspv1_s, edspv1_c,
 edspv2_s, edspv2_c] = [pg.read(path, expno) for expno in
                        (11001, 11002, 13001, 13002, 15001, 15002, 17001, 17002,
                         12001, 12002, 14001, 14002, 16001, 16002, 18001, 18002)]

fig, axs = pg.subplots2d(1, 3, figsize=(10, 5))

xlabels = [
    r"NOAH-2 $\rm S^{+}_{crk}C^{c}$ ($\Delta' = 1/(4J)$)",
    r"NOAH-2 $\rm S^{+}_{1}C^{c}$ ($\Delta' = 1/(4J)$)",
    r"NOAH-2 $\rm S^{+}_{2}C^{c}$ ($\Delta' = 1/(4J)$)",
]
ylabels = [r"intensity vs NOAH-2 $\rm SC^{c}$"] * 3
          
datasets = [
    [crk_s, crk_c],
    [spv1_s, spv1_c],
    [spv2_s, spv2_c],
]
editeds = [False] * 3
ref_datasets = [[sc_s, sc_c]] * 3

for ax, xlabel, ylabel, dataset, ref_dataset, edited in zip(axs,
                                                            xlabels, ylabels,
                                                            datasets, ref_datasets,
                                                            editeds):
    hsqc_cosy_stripplot(molecule=Andro,
                        datasets=dataset, ref_datasets=ref_dataset,
                        xlabel=xlabel, ylabel=ylabel,
                        ax=ax, edited=edited, ncol=1, loc="upper right")

pg.label_axes(axs, fontsize=14, fstr="({})", fontweight="bold")

for ax in axs[1:]:
    ax.yaxis.set_visible(False)

for ax in axs:
    ax.legend().set_visible(False)
    ax.set_ylim(-0.3, 2.4)
    pg.style_axes(ax, "plot")

# make general legend
handles, labels = ax.get_legend_handles_labels()
for handle in handles[0:4]:
    handle.set(sizes=[15])
fig.legend(handles[0:4], ["HSQC CH", "HSQC CH$_2$", "HSQC CH$_3$", "COSY"],
           ncol=4, bbox_to_anchor=(0.54, 0.99),
           loc="upper center")
pg.cleanup_figure()

# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
