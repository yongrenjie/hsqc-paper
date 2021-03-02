from pathlib import Path
import matplotlib.pyplot as plt
import penguins as pg
from penguins.private import nmrd
from penguins.private import Andrographolide as Andro
from penguins.private import hsqc_cosy_stripplot
plt.style.use(Path(__file__).parent / "helv.mplstyle")

path = nmrd() / "210126-7a-hsqct-full"

[sc_s, sc_c,
 stp_s, stp_c,
 st1_s, st1_c,
 st09_s, st09_c] = [pg.read(path, expno) for expno in
                                          (3001, 3002,
                                           43002, 43003,
                                           27002, 27003,
                                           28002, 28003)]

fig, axs = pg.subplots2d(1, 3, figsize=(9, 4))
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[stp_s, stp_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel=r"X = seHSQC-TOCSY",
                    ylabel=r"intensity vs NOAH-2 $\rm SC^{c}$",
                    ax=axs[0],
                    ncol=1, loc="upper right")
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[st1_s, st1_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel=r"X = HSQC-TOCSY ($f = 1$)",
                    ylabel=r"intensity vs NOAH-2 $\rm SC^{c}$",
                    ax=axs[1],
                    ncol=1, loc="upper right")
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[st09_s, st09_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel=r"X = HSQC-TOCSY ($f = 0.9$)",
                    ylabel=r"intensity vs NOAH-2 $\rm SC^{c}$",
                    ax=axs[2],
                    ncol=1, loc="upper right")
pg.label_axes(axs, fontsize=14, fstr="({})", fontweight="bold")

for ax in axs[1:]:
    ax.yaxis.set_visible(False)
for ax in axs:
    ax.legend().set_visible(False)
    ax.set_ylim(-0.1, 1.5)
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
