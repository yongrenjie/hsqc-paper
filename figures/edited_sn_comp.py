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
 spv2_s, spv2_c] = [pg.read(path, expno) for expno in
                                          (12001, 12002,
                                           20001, 20002,
                                           22001, 22002,
                                           24001, 24002)
                                          ]

fig, axs = pg.subplots(1, 3, figsize=(9, 4))
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[crk_s, crk_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel=r"edited NOAH-2 $\rm S^{+}_{crk}C^{c}$",
                    ylabel=r"intensity vs edited NOAH-2 $\rm SC^{c}$",
                    ax=axs[0],
                    edited=True,
                    ncol=1, loc="upper right")
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[spv1_s, spv1_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel=r"edited NOAH-2 $\rm S^{+}_{1}C^{c}$",
                    ylabel=r"intensity vs edited NOAH-2 $\rm SC^{c}$",
                    ax=axs[1],
                    edited=True,
                    ncol=1, loc="upper right")
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[spv2_s, spv2_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel=r"edited NOAH-2 $\rm S^{+}_{2}C^{c}$",
                    ylabel=r"intensity vs edited NOAH-2 $\rm SC^{c}$",
                    ax=axs[2],
                    edited=True,
                    ncol=1, loc="upper right")
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
