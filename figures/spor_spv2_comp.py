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
spv2c_s = pg.read(p, 23001)
spv2c_c = pg.read(p, 23002)

fig = plt.figure(figsize=(6.5, 6))
gs = fig.add_gridspec(6, 6)
axs = [
    fig.add_subplot(gs[:4,:3]),
    fig.add_subplot(gs[:4,3:]),
    fig.add_subplot(gs[4:,:2]),
    fig.add_subplot(gs[4:,2:4]),
    fig.add_subplot(gs[4:,4:])
]
# CRK seHSQC vs standard HSQC
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[sporc_s, sporc_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel="CRK seHSQC + CLIP-COSY",
                    ylabel="intensity vs NOAH HSQC + CLIP-COSY",
                    ax=axs[0],
                    ncol=1, loc="upper right", size=4)
# NOAH seHSQC vs standard HSQC
hsqc_cosy_stripplot(molecule=Andro,
                    datasets=[spv2c_s, spv2c_c],
                    ref_datasets=[sc_s, sc_c],
                    xlabel="NOAH seHSQC + CLIP-COSY",
                    ylabel="intensity vs NOAH HSQC + CLIP-COSY",
                    ax=axs[1],
                    ncol=1, loc="upper right", size=4)
axs[1].yaxis.set_visible(False)
for ax in axs[0:2]:
    ax.set_ylim(-0.3, 2.6)
    pg.style_axes(ax, "plot")

# Projections
dark = pg.color_palette("dark")
bright = pg.color_palette("bright")
# CH
b = (3.08, 3.38)
c1, c2 = dark[0], bright[0]
sp_slice = spv2c_s.slice(axis=1, ppm=78.9)
s_slice = sc_s.slice(axis=1, ppm=78.9)
s_slice.stage(ax=axs[2], bounds=b, linestyle="--", color=c2)
sp_slice.stage(ax=axs[2], bounds=b, color=c1)
s_int = s_slice.integrate(bounds=b, mode="max")
sp_int = sp_slice.integrate(bounds=b, mode="max")
axs[2].text(x=3.23-0.03, y=s_int, s="HSQC", color=c2, horizontalalignment="left",
            verticalalignment="top", fontsize=8)
axs[2].text(x=3.23-0.02, y=sp_int, s="NOAH seHSQC", color=c1, horizontalalignment="left",
            verticalalignment="top", fontsize=8)
axs[2].text(x=3.23-0.02, y=sp_int-1.5e4, s=f"({sp_int/s_int:.2f}×)",
            color=c1, horizontalalignment="left",
            verticalalignment="top", fontsize=8)

# CH2
b = (1.49, 1.79)
c1, c2 = dark[1], bright[1]
sp_slice = spv2c_s.slice(axis=1, ppm=28.45)
s_slice = sc_s.slice(axis=1, ppm=28.45)
s_slice.stage(ax=axs[3], bounds=b, linestyle="--", color=c2)
sp_slice.stage(ax=axs[3], bounds=b, color=c1)
s_int = s_slice.integrate(bounds=b, mode="max")
sp_int = sp_slice.integrate(bounds=b, mode="max")
axs[3].text(x=1.64-0.02, y=sp_int, s=f"({sp_int/s_int:.2f}×)",
            color=c1, horizontalalignment="left",
            verticalalignment="top", fontsize=8)

# COSY
b = (1.65, 2.05)
c1, c2 = dark[3], bright[3]
sp_slice = spv2c_c.slice(axis=1, ppm=1.36)
s_slice = sc_c.slice(axis=1, ppm=1.36)
s_slice.stage(ax=axs[4], bounds=b, linestyle="--", color=c2)
sp_slice.stage(ax=axs[4], bounds=b, color=c1)
s_int1 = s_slice.integrate(bounds=(1.72, 1.76), mode="max")
s_int2 = s_slice.integrate(bounds=(1.92, 1.96), mode="max")
sp_int1 = sp_slice.integrate(bounds=(1.72, 1.76), mode="max")
sp_int2 = sp_slice.integrate(bounds=(1.92, 1.96), mode="max")
axs[4].text(x=1.74-0.02, y=sp_int1-2e4, s=f"({sp_int1/s_int1:.2f}×)",
            color=c1, horizontalalignment="left",
            verticalalignment="top", fontsize=8)
axs[4].text(x=1.94+0.02, y=sp_int2-2e4, s=f"({sp_int2/s_int2:.2f}×)",
            color=c1, horizontalalignment="right",
            verticalalignment="top", fontsize=8)

pg.mkplots(axs[2:])
pg.label_axes(axs, fstr="({})", fontsize=14, fontweight="bold")
# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
