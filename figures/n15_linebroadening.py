from pathlib import Path
import penguins as pg
from penguins.private import Gramicidin as Grami
import matplotlib.pyplot as plt
from penguins.private import nmrd

plt.rcParams["font.family"] = "Source Sans Pro"

path = nmrd() / "201017-7g-n15-sehsqc-full"
mspv2cc_spv2 = pg.read(path, 12002)
sspv2cc_spv2 = pg.read(path, 22002)
spv2spv2cc_spv2 = pg.read(path, 42002)

fig, axs = pg.subplots(2, 3, figsize=(12, 6.5),
                       gridspec_kw={"height_ratios": [2, 1]})
dss = [mspv2cc_spv2, sspv2cc_spv2, spv2spv2cc_spv2]
titles = [r"after $^{15}$N HMQC",
          r"after $^{15}$N HSQC",
          r"after $^{15}$N seHSQC"]
for ds, ax in zip(dss, axs[0]):
    ds.stage(ax, levels=7e3, f1_bounds="15..65", f2_bounds="0.5..5")
for ds, ax in zip(dss, axs[1]):
    ds.f1projp().stage(ax, bounds="15..65")

pg.mkplots(axs[0], titles)
pg.mkplots(axs[1])
pg.label_axes(axs, fontsize=16, fstr="({})", fontweight="bold")

ymin, ymax = axs[1][0].get_ylim()
for ax in axs[1]:
    ax.set_ylim((ymin, ymax))

# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype), dpi=500)

# print relative integrals
x = Grami.hsqc.rel_ints_df(sspv2cc_spv2, mspv2cc_spv2)
print("HSQC vs HMQC")
print(x)
print(x.mean())
y = Grami.hsqc.rel_ints_df(spv2spv2cc_spv2, mspv2cc_spv2)
print("seHSQC vs HMQC")
print(y)
print(y.mean())
