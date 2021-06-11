from pathlib import Path
import penguins as pg
from penguins.private import Gramicidin as Grami
import matplotlib.pyplot as plt
from penguins.private import nmrd
plt.style.use(Path(__file__).parent / "helv.mplstyle")

path = nmrd() / "201017-7g-n15-sehsqc-full"
mspv2cc_spv2 = pg.read(path, 12002)
sspv2cc_spv2 = pg.read(path, 22002)
spv2spv2cc_spv2 = pg.read(path, 42002)

fig, axs = pg.subplots2d(2, 3, figsize=(12, 6.5), height_ratios=[2, 1])
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

ymin, ymax = axs[1][0].get_ylim()
for ax in axs[1]:
    ax.set_ylim((ymin, ymax))

for ax in axs[0]:
    pg.ymove(ax, "topright")
pg.label_axes(axs, fontsize=14, fstr="({})", fontweight="bold")
pg.cleanup_axes()

# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))

# print relative integrals
ref_spv2cc_spv2 = pg.read(path, 4001)

print("\n----------------------------------------")
print("HSQC vs HMQC")
x = Grami.hsqc.rel_ints_df(sspv2cc_spv2, mspv2cc_spv2)
print(x.mean())

print("\n----------------------------------------")
print("HSQC vs reference (no 15N module)")
y1 = Grami.hsqc.rel_ints_df(sspv2cc_spv2, ref_spv2cc_spv2)
print(y1.mean())

print("\n----------------------------------------")
print("seHSQC vs HMQC")
y = Grami.hsqc.rel_ints_df(spv2spv2cc_spv2, mspv2cc_spv2)
print(y.mean())

print("\n----------------------------------------")
print("short AQ (Zolmi): HSQC vs HMQC")
from penguins.private import Zolmitriptan as Zolmi
short_aq_hmqc = pg.read(nmrd() / "200926-7z-n15-sehsqc-full", 15002)
short_aq_hsqc = pg.read(nmrd() / "200926-7z-n15-sehsqc-full", 25002)
z = Zolmi.hsqc.rel_ints_df(short_aq_hsqc, short_aq_hmqc)
print(z.mean())
