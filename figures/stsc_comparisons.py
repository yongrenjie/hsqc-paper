from pathlib import Path
import numpy as np
import penguins as pg
from penguins.private import nmrd
from penguins.private import Andrographolide as Andro
import matplotlib.pyplot as plt
plt.style.use(Path(__file__).parent / "helv.mplstyle")

path = nmrd() / "201010-7a-hsqctocsy"

# Read reference datasets and get reference intensities
ref_s, ref_c = [pg.read(path, expno) for expno in (1001, 1002)]
ref_s_ints = Andro.hsqc.integrate(ref_s)
ref_c_ints = Andro.cosy.integrate(ref_c)

# Read in datasets of interest
noah_ssc_s = [pg.read(path, expno * 1000 + 2) for expno in range(11, 18)]
noah_ssc_c = [pg.read(path, expno * 1000 + 3) for expno in range(11, 18)]
noah_stsc_s = [pg.read(path, expno * 1000 + 2) for expno in range(21, 28)]
noah_stsc_c = [pg.read(path, expno * 1000 + 3) for expno in range(21, 28)]

# seHSQC in slot 2
noah_sspc_sp = [pg.read(path, expno * 1000 + 2) for expno in range(31, 38)]
noah_sspc_c = [pg.read(path, expno * 1000 + 3) for expno in range(31, 38)]
noah_stspc_sp = [pg.read(path, expno * 1000 + 2) for expno in range(41, 48)]
noah_stspc_c = [pg.read(path, expno * 1000 + 3) for expno in range(41, 48)]

# Calculate intensities (averaged over all peaks) for datasets of interest
get_rel_s_ints = lambda ds: np.mean(Andro.hsqc.integrate(ds) / ref_s_ints)
get_rel_c_ints = lambda ds: np.mean(Andro.cosy.integrate(ds) / ref_c_ints)
mkarray = lambda fn, dss: np.array(list(map(fn, dss)))

noah_ssc_s_ints = mkarray(get_rel_s_ints, noah_ssc_s)
noah_ssc_c_ints = mkarray(get_rel_c_ints, noah_ssc_c)
noah_stsc_s_ints = mkarray(get_rel_s_ints, noah_stsc_s)
noah_stsc_c_ints = mkarray(get_rel_c_ints, noah_stsc_c)
noah_sspc_sp_ints = mkarray(get_rel_s_ints, noah_sspc_sp)
noah_sspc_c_ints = mkarray(get_rel_c_ints, noah_sspc_c)
noah_stspc_sp_ints = mkarray(get_rel_s_ints, noah_stspc_sp)
noah_stspc_c_ints = mkarray(get_rel_c_ints, noah_stspc_c)

# Get values of cnst32
cnst32s = [ds["cnst32"] for ds in noah_ssc_s]

# Plot them.
fig, axs = pg.subplots(1, 2, sharey=True)
deep = pg.color_palette("deep")
pastel = pg.color_palette("pastel")
for (ax,
     s1_ints, s2_ints,
     c1_ints, c2_ints,
     label2, title) in zip(axs,
                           [noah_ssc_s_ints, noah_sspc_sp_ints],
                           [noah_stsc_s_ints, noah_stspc_sp_ints],
                           [noah_ssc_c_ints, noah_sspc_c_ints],
                           [noah_stsc_c_ints, noah_stspc_c_ints],
                           ["HSQC", "seHSQC"],
                           ["NOAH-3 StSCc", "NOAH-3 StSpCc"]):
    # Plot NOAH intensities
    ax.plot(cnst32s, s1_ints, linestyle="--", linewidth=0.5, color=pastel[1])
    ax.plot(cnst32s, s2_ints, color=deep[1])
    ax.plot(cnst32s, c1_ints, linestyle="--", linewidth=0.5, color=pastel[2])
    ax.plot(cnst32s, c2_ints, color=deep[2])
    # Twiddle with axes properties.
    ax.set(xlabel="value of $f$", ylabel="Relative intensity",
           ylim=(-0.05, 1.15), title=title)
    ax.legend(["", f"{label2} #2", "", "COSY"], loc="lower right")
    ax.invert_xaxis()
    ax.label_outer()
    pg.style_axes(ax, "plot")

pg.label_axes(axs, fstr="({})", fontweight="bold", fontsize=14)
pg.show()
# for filetype in [".png", ".svg"]:
#     pg.savefig(str(Path(__file__)).replace(".py", filetype))
