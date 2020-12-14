from pathlib import Path
import numpy as np
import penguins as pg
from penguins.private import nmrd
from penguins.private import Andrographolide as Andro
import matplotlib.pyplot as plt
plt.style.use(Path(__file__).parent / "helv.mplstyle")

# Just change these...
path = nmrd() / "201206-7a-hsqct-full"
ref_noah_sc_expno = 3
ssc_expnos = range(11, 19)
sspc_expnos = range(19, 27)
stsc_expnos = range(27, 35)
stspc_expnos = range(35, 43)


# Read reference datasets and get reference intensities
ref_s, ref_c = [pg.read(path, expno)
                for expno in (ref_noah_sc_expno * 1000 + 1,
                              ref_noah_sc_expno * 1000 + 2)]
ref_s_ints = Andro.hsqc.integrate(ref_s)
ref_c_ints = Andro.cosy.integrate(ref_c)

# Read in datasets of interest
noah_ssc_s = [pg.read(path, expno * 1000 + 2) for expno in ssc_expnos]
noah_ssc_c = [pg.read(path, expno * 1000 + 3) for expno in ssc_expnos]
noah_stsc_s = [pg.read(path, expno * 1000 + 2) for expno in stsc_expnos]
noah_stsc_c = [pg.read(path, expno * 1000 + 3) for expno in stsc_expnos]

# seHSQC in slot 2
noah_sspc_sp = [pg.read(path, expno * 1000 + 2) for expno in sspc_expnos]
noah_sspc_c = [pg.read(path, expno * 1000 + 3) for expno in sspc_expnos]
noah_stspc_sp = [pg.read(path, expno * 1000 + 2) for expno in stspc_expnos]
noah_stspc_c = [pg.read(path, expno * 1000 + 3) for expno in stspc_expnos]

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
                           ["S", r"S^{+}"],
                           ["With HSQC as second module", "With seHSQC as second module"]):
    # Plot NOAH intensities
    ax.plot(cnst32s, s1_ints, linestyle="--", color=pastel[1], marker="o")
    ax.plot(cnst32s, s2_ints, color=deep[1], marker="o")
    ax.plot(cnst32s, c1_ints, linestyle="--", color=pastel[2], marker="x")
    ax.plot(cnst32s, c2_ints, color=deep[2], marker="x")
    # Twiddle with axes properties.
    ax.set(xlabel="value of $f$",
           ylabel="Intensity relative to NOAH-2 SCc",
           ylim=(-0.05, 1.15), title=title)
    ax.legend([rf"S$\bf {label2}$$\rm C^c$", rf"$\rm S^T$$\bf {label2}$$\rm C^c$",
               rf"S$\rm {label2}$$\bf C^c$", rf"$\rm S^T$$\rm {label2}$$\bf C^c$",],
              loc="lower right", ncol=2)
    ax.invert_xaxis()
    ax.label_outer()
    pg.style_axes(ax, "plot")

pg.label_axes(axs, fstr="({})", fontweight="bold", fontsize=14)
# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
