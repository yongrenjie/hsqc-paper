from pathlib import Path
import matplotlib.pyplot as plt
import penguins as pg
from penguins.private import nmrd
from penguins.private import Gramicidin as Grami, Zolmitriptan as Zolmi
from penguins.private import hsqc_stripplot
plt.style.use(Path(__file__).parent / "helv.mplstyle")

g_path = nmrd() / "201017-7g-n15-sehsqc-full"
z_path = nmrd() / "200926-7z-n15-sehsqc-full"

[g_ref_spv2, g_m_spv2, g_spv2_spv2] = [pg.read(g_path, expno) for expno in
                                       (4001, 12002, 42002)]
[z_ref_spv2, z_m_spv2, z_spv2_spv2] = [pg.read(z_path, expno) for expno in
                                       (4001, 12002, 42002)]

_, axs = pg.subplots(2, 1, figsize=(5, 8))
hsqc_stripplot(molecule=Grami,
               datasets=[g_m_spv2, g_spv2_spv2],
               ref_dataset=g_ref_spv2,
               expt_labels=["HMQC", "seHSQC"],
               xlabel=r"$^{15}$N module",
               ylabel=r"Relative intensity of $^{13}$C seHSQC",
               ax=axs[0],
               loc="upper center")
hsqc_stripplot(molecule=Zolmi,
               datasets=[z_m_spv2, z_spv2_spv2],
               ref_dataset=z_ref_spv2,
               expt_labels=["HMQC", "seHSQC"],
               xlabel=r"$^{15}$N module",
               ylabel=r"Relative intensity of $^{13}$C seHSQC",
               ax=axs[1],
               loc="upper center")
for ax in axs:
    ax.set_ylim(-0.3, 2.4)
    pg.style_axes(ax, "plot")

pg.label_axes(axs, fontsize=14, fstr="({})", fontweight="bold")
# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
