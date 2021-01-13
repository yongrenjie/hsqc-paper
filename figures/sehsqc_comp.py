import numpy as np
import penguins as pg
from penguins.private import Andrographolide as Andro
from penguins.private import nmrd, hsqc_cosy_stripplot
from pathlib import Path
import matplotlib.pyplot as plt

plt.style.use(Path(__file__).parent / "helv.mplstyle")
plt.rcParams["legend.labelspacing"] = 0.2
plt.rcParams["legend.handlelength"] = 0.5

p = nmrd() / "201115-7a-c13-sehsqc-full"
sc_s = pg.read(p, 11001)
sc_c = pg.read(p, 11002)
sporc_s = pg.read(p, 19001)
sporc_c = pg.read(p, 19002)
spv1c_s = pg.read(p, 21001)
spv1c_c = pg.read(p, 21002)
spv2c_s = pg.read(p, 23001)
spv2c_c = pg.read(p, 23002)

fig, axs = plt.subplots(2, 3, figsize=(6.5, 6),
                        gridspec_kw={"height_ratios": [2, 1]}
                        )
# CRK seHSQC vs standard HSQC
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[sporc_s, sporc_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel=r"NOAH-2 $\rm S^{+}_{crk}C^c$",
                    ylabel=r"intensity vs NOAH-2 $\rm SC^c$",
                    ax=axs[0][0],
                    size=4,
                    font_kwargs={"size": 8.5}
                    )
# NOAH seHSQC v1, vs standard HSQC
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[spv1c_s, spv1c_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel=r"NOAH-2 $\rm S^{+}_{1}C^c$",
                    ylabel=r"intensity vs NOAH-2 $\rm SC^c$",
                    ax=axs[0][1],
                    size=4,
                    font_kwargs={"size": 8.5}
                    )
# NOAH seHSQC v2, vs standard HSQC
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[spv2c_s, spv2c_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel=r"NOAH-2 $\rm S^{+}_{2}C^c$",
                    ylabel=r"intensity vs NOAH-2 $\rm SC^c$",
                    ax=axs[0][2],
                    size=4,
                    font_kwargs={"size": 8.5}
                    )
axs[0][1].yaxis.set_visible(False)
axs[0][2].yaxis.set_visible(False)
for ax in axs[0]:
    ax.legend().set_visible(False)
    ax.set_xlim(-0.4, 0.4)
    ax.set_ylim(-0.3, 2.4)
    pg.style_axes(ax, "plot")


handles, labels = ax.get_legend_handles_labels()
for handle in handles[0:4]:
    handle.set(sizes=[15])
fig.legend(handles[0:4], ["HSQC CH", "HSQC CH$_2$", "HSQC CH$_3$", "COSY"],
           ncol=4, fontsize=10,
           bbox_to_anchor=(0.54, 0.99),
           loc="upper center")

# Projections
dark = pg.color_palette("dark")
bright = pg.color_palette("bright")
# CH
b = (3.08, 3.38)
c1, c2 = dark[0], bright[0]
sp_slice = spv2c_s.slice(axis=1, ppm=78.9)
s_slice = sc_s.slice(axis=1, ppm=78.9)
s_slice.stage(ax=axs[1][0], bounds=b, linestyle="--", color=c2)
sp_slice.stage(ax=axs[1][0], bounds=b, color=c1)
s_int = s_slice.integrate(bounds=b, mode="max")
sp_int = sp_slice.integrate(bounds=b, mode="max")
axs[1][0].text(x=3.23-0.03, y=s_int, s="HSQC", color=c2, horizontalalignment="left",
            verticalalignment="top", fontsize=8)
axs[1][0].text(x=3.23-0.02, y=sp_int, s=r"ZIP-seHSQC ($\rm S^{+}_{2}$)", color=c1, horizontalalignment="left",
            verticalalignment="top", fontsize=8)
axs[1][0].text(x=3.23-0.02, y=sp_int-1.8e4, s=f"({sp_int/s_int:.2f}×)",
            color=c1, horizontalalignment="left",
            verticalalignment="top", fontsize=8)

# CH2
b = (1.49, 1.79)
c1, c2 = dark[1], bright[1]
sp_slice = spv2c_s.slice(axis=1, ppm=28.45)
s_slice = sc_s.slice(axis=1, ppm=28.45)
s_slice.stage(ax=axs[1][1], bounds=b, linestyle="--", color=c2)
sp_slice.stage(ax=axs[1][1], bounds=b, color=c1)
s_int = s_slice.integrate(bounds=b, mode="max")
sp_int = sp_slice.integrate(bounds=b, mode="max")
axs[1][1].text(x=1.64-0.02, y=sp_int, s=f"({sp_int/s_int:.2f}×)",
            color=c1, horizontalalignment="left",
            verticalalignment="top", fontsize=8)

# COSY
b = (1.65, 2.05)
c1, c2 = dark[3], bright[3]
sp_slice = spv2c_c.slice(axis=1, ppm=1.36)
s_slice = sc_c.slice(axis=1, ppm=1.36)
s_slice.stage(ax=axs[1][2], bounds=b, linestyle="--", color=c2)
sp_slice.stage(ax=axs[1][2], bounds=b, color=c1)
s_int1 = s_slice.integrate(bounds=(1.72, 1.76), mode="max")
s_int2 = s_slice.integrate(bounds=(1.92, 1.96), mode="max")
sp_int1 = sp_slice.integrate(bounds=(1.72, 1.76), mode="max")
sp_int2 = sp_slice.integrate(bounds=(1.92, 1.96), mode="max")
axs[1][2].text(x=1.74-0.02, y=sp_int1-2e4, s=f"({sp_int1/s_int1:.2f}×)",
            color=c1, horizontalalignment="left",
            verticalalignment="top", fontsize=8)
axs[1][2].text(x=1.94+0.02, y=sp_int2-2e4, s=f"({sp_int2/s_int2:.2f}×)",
            color=c1, horizontalalignment="right",
            verticalalignment="top", fontsize=8)

pg.mkplots(axs[1])
pg.label_axes(axs, fstr="({})", fontsize=14, fontweight="bold")
pg.cleanup_figure()

# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
