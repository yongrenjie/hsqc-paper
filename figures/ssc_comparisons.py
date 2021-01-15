from pathlib import Path
import numpy as np
import penguins as pg
from penguins.private import nmrd
from penguins.private import Andrographolide as Andro
import matplotlib.pyplot as plt
plt.style.use(Path(__file__).parent / "helv.mplstyle")
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
fig, axs = pg.subplots(1, 3, sharey=True,
                       gridspec_kw={"width_ratios": [0.5, 4, 4]},
                       figsize=(8, 4))
deep = pg.color_palette("deep")
# Axes #1 - MFA intensities
# Plot MFA intensities and line to guide the eye
for i, c, m in zip((mfa_s1_int, mfa_s2_int, mfa_c_int), deep[0:3], "oox"):
    axs[0].plot(1, i, marker=m, color=c)
    axs[0].axhline(y=i, color=c, linestyle="--", linewidth=0.5)
    axs[0].set(xticks=[1], xticklabels=["MFA"])
    axs[0].set(ylabel="Relative intensity",
               ylim=(-0.05, 1.15), title="MFA")
# Axes #2 and #3 - NOAH intensities, but with MFA dotted lines
for (ax, s1_ints, s2_ints,
     c_ints, label1, label2, title) in zip(axs[1:],
                                           [noah_s1_ints, noah_sps1_ints],
                                           [noah_s2_ints, noah_sps2_ints],
                                           [noah_c_ints, noah_spc_ints],
                                           ["HSQC #1", "HSQC"],
                                           ["HSQC #2", "seHSQC"],
                                           [r"NOAH-3 SS$\rm C^c$", r"NOAH-3 S$\rm S^{+}_{2}C^c$"]):
    # Plot NOAH intensities
    for i, c, m in zip((s1_ints, s2_ints, c_ints), deep[0:3], "oox"):
        ax.plot(cnst32s, i, marker=m, color=c)
    for i, c in zip((mfa_s1_int, mfa_s2_int, mfa_c_int), deep[0:3]):
        ax.axhline(y=i, color=c, linestyle="--", linewidth=0.5)
    # Twiddle with axes properties.
    ax.set(xlabel="value of $f$", title=title)
    ax.legend([label1, label2, "COSY"], loc="lower right")
    ax.invert_xaxis()

for ax in axs.flat:
    ax.label_outer()
    pg.style_axes(ax, "plot")

# Because Axes #1 is so small, we need to bump up the x-value on the text.
pg.label_axes(axs[0], fstr="({})", start=1, fontweight="bold", fontsize=14,
              x=0.15)
pg.label_axes(axs[1:], fstr="({})", start=2, fontweight="bold", fontsize=14)
# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
