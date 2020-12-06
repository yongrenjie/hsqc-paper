from pathlib import Path
import numpy as np
import penguins as pg
from penguins.private import nmrd
from penguins.private import Andrographolide as Andro
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Source Sans Pro"
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.it"] = "Source Sans Pro:italic"
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

path = nmrd() / "201010-7a-hsqctocsy"

# Read reference datasets and get reference intensities
ref_s, ref_c = [pg.read(path, expno) for expno in (1001, 1002)]
ref_s_ints = Andro.hsqc.integrate(ref_s)
ref_c_ints = Andro.cosy.integrate(ref_c)

# Read in datasets of interest
mfa_s1, mfa_s2, mfa_c = [pg.read(path, expno) for expno in (6001, 6002, 6003)]
noah_s1 = [pg.read(path, expno * 1000 + 1) for expno in range(11, 18)]
noah_s2 = [pg.read(path, expno * 1000 + 2) for expno in range(11, 18)]
noah_c = [pg.read(path, expno * 1000 + 3) for expno in range(11, 18)]

# seHSQC in slot 2
noah_sps1 = [pg.read(path, expno * 1000 + 1) for expno in range(31, 38)]
noah_sps2 = [pg.read(path, expno * 1000 + 2) for expno in range(31, 38)]
noah_spc = [pg.read(path, expno * 1000 + 3) for expno in range(31, 38)]

# Calculate intensities (averaged over all peaks) for datasets of interest
get_rel_s_ints = lambda ds: np.mean(Andro.hsqc.integrate(ds) / ref_s_ints)
get_rel_c_ints = lambda ds: np.mean(Andro.cosy.integrate(ds) / ref_c_ints)
mfa_s1_int = get_rel_s_ints(mfa_s1)
mfa_s2_int = get_rel_s_ints(mfa_s2)
mfa_c_int = get_rel_c_ints(mfa_c)
noah_s1_ints = list(map(get_rel_s_ints, noah_s1))
noah_s2_ints = list(map(get_rel_s_ints, noah_s2))
noah_c_ints = list(map(get_rel_c_ints, noah_c))
noah_sps1_ints = list(map(get_rel_s_ints, noah_sps1))
noah_sps2_ints = list(map(get_rel_s_ints, noah_sps2))
noah_spc_ints = list(map(get_rel_c_ints, noah_spc))

# Get values of cnst32
cnst32s = [ds["cnst32"] for ds in noah_c]

# Plot them. This code is modified from 201007 lab book.
fig, axs = pg.subplots(1, 2, sharey=True)
deep = pg.color_palette("deep")
for (ax, s1_ints, s2_ints,
     c_ints, label2, title) in zip(axs,
                                   [noah_s1_ints, noah_sps1_ints],
                                   [noah_s2_ints, noah_sps2_ints],
                                   [noah_c_ints, noah_spc_ints],
                                   ["HSQC", "seHSQC"],
                                   ["NOAH-3 SSCc", "NOAH-3 SSpCc"]):
    # Plot NOAH intensities
    for i, c in zip((s1_ints, s2_ints, c_ints), deep[0:3]):
        ax.plot(cnst32s, i, marker='o', color=c)
    # Plot MFA intensities and line to guide the eye
    for i, c in zip((mfa_s1_int, mfa_s2_int, mfa_c_int), deep[0:3]):
        ax.plot(1.1, i, marker='o', color=c)
        ax.axhline(y=i, color=c, linestyle="--", linewidth=0.5)
    # Twiddle with axes properties.
    ax.set(xlabel="value of $f$", ylabel="Relative intensity",
           ylim=(-0.05, 1.15), title=title)
    ax.legend(["HSQC #1", f"{label2} #2", "COSY"], loc="lower right")
    ax.set_xticklabels(["0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0", "MFA"])
    ax.invert_xaxis()
    ax.label_outer()
    pg.style_axes(ax, "plot")

pg.label_axes(axs, fstr="({})", fontweight="bold", fontsize=16)
# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype), dpi=500)
