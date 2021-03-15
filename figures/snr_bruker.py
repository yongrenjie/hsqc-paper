from pathlib import Path
import numpy as np
import penguins as pg
from penguins.private import nmrd
from penguins.private import Zolmitriptan as Zolmi
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
plt.style.use(Path(__file__).parent / "helv.mplstyle")

path = nmrd() / "210213-7z-noah4-snr"

# noah-4 with 2 scans - 17 min 28 sec
noah4_2scans = (17*60+28, [pg.read(path, e) for e in range(1001, 1005)])
# noah-4 with 8 scans - 68 min 16 sec
noah4_8scans = (68*60+16, [pg.read(path, e) for e in range(2001, 2005)])
# individual noah modules with 2 scans each
# 14 min 36 sec, 14 min 26 sec, 14 min 13 sec, 15 min 27 sec
# total: 58 min 42 sec
modules_2scans = (58*60+42, [pg.read(path, e) for e in range(11, 15)])
# individual bruker recommended experiments with 2 scans each
# 14 min 5 sec, 14 min 1 sec, 13 min 57 sec, 14 min 32 sec
# total: 56 min 35 sec
bruker_2scans = (56*60+35, [pg.read(path, e) for e in range(21, 25)])

def get_ints(dss, overall_label, noise_level=1):
    reference_dss = bruker_2scans
    nhsqc_ints = (Zolmi.nhsqc.integrate(dss[1][0]) /
                  Zolmi.nhsqc.integrate(reference_dss[1][0]))
    chsqc_ints = (Zolmi.hsqc.integrate(dss[1][1], edited=True) /
                  Zolmi.hsqc.integrate(reference_dss[1][1], edited=True))
    cosy_ints = (Zolmi.cosy.integrate(dss[1][2]) /
                 Zolmi.cosy.integrate(reference_dss[1][2]))
    tocsy_ints = (Zolmi.tocsy_35ms.integrate(dss[1][3]) /
                  Zolmi.tocsy_35ms.integrate(reference_dss[1][3]))
    time_saving = dss[0] / reference_dss[0]

    def get_expt_df(ints, expt_label):
        n = ints.size
        e_t = ints / (np.sqrt(time_saving) * noise_level)
        return pd.DataFrame.from_dict({"e_t": e_t,
                                       "expt": [expt_label] * n,
                                       "sequence": [overall_label] * n})
    dfs = [get_expt_df(ints, expt_label)
           for ints, expt_label in zip([nhsqc_ints, chsqc_ints, cosy_ints, tocsy_ints],
                                       [r"$^{15}$N seHSQC", r"$^{13}$C seHSQC",
                                        "COSY", "TOCSY"])]
    return pd.concat(dfs)

fig, ax = plt.subplots(figsize=(9, 4))
data = pd.concat((get_ints(noah4_2scans, "NOAH-4 $\\rm S_{N}S^{+}_{2}CT$"),
                  get_ints(modules_2scans, "individual NOAH modules"),
                  get_ints(bruker_2scans, "standard 2D experiments")),
                 axis=0)
sns.barplot(x="sequence", y="e_t", hue="expt", data=data, palette="deep")
ax.axhline(y=1, color="grey", linestyle="--")
ax.set_xlabel("type of experiment")
ax.set_ylabel("relative sensitivity / unit time")
ax.legend().set_visible(False)
leg = fig.legend(loc="upper center", ncol=4)
pg.style_axes(ax, "plot")
pg.cleanup_figure()

# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
