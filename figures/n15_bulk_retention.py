import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt
import penguins as pg
import pandas as pd
from penguins.private import nmrd
from penguins.private import Gramicidin as Grami, Zolmitriptan as Zolmi
plt.style.use(Path(__file__).parent / "helv.mplstyle")

g_path = nmrd() / "201017-7g-n15-sehsqc-full"
z_path = nmrd() / "200926-7z-n15-sehsqc-full"

# This hsqc_stripplot() is different from penguins' version!
def hsqc_stripplot(molecule,
                   datasets,
                   ref_dataset,
                   expt_labels,
                   xlabel="Experiment",
                   ylabel="Intensity",
                   title="",
                   edited=False,
                   show_averages=True,
                   ncol=3,
                   loc="upper center",
                   ax=None,
                   **kwargs):
    # Stick dataset/label into a list if needed
    # if isinstance(datasets, ds.Dataset2D):
    #     datasets = [datasets]
    if isinstance(expt_labels, str):
        expt_labels = [expt_labels]
    # Calculate dataframes of relative intensities.
    rel_ints_dfs = [molecule.hsqc.rel_ints_df(dataset=ds,
                                              ref_dataset=ref_dataset,
                                              label=label,
                                              edited=edited)
                    for (ds, label) in zip(datasets, expt_labels)]
    all_dfs = pd.concat(rel_ints_dfs)

    # Calculate the average integrals by multiplicity
    avgd_ints = all_dfs.groupby("expt").mean()
    avgd_ints.drop(columns=["f1", "f2"], inplace=True)

    # Get currently active axis if none provided
    if ax is None:
        ax = plt.gca()

    # Plot the intensities.
    stripplot_alpha = 0.3 if show_averages else 0.8
    sns.stripplot(x="expt", y="int",
                  zorder=0, alpha=stripplot_alpha,
                  dodge=True, data=all_dfs, ax=ax, **kwargs)
    if show_averages:
        sns.pointplot(x="expt", y="int", zorder=1,
                      dodge=0.5, data=all_dfs, ax=ax, join=False,
                      markers='_', palette="dark", ci=None, scale=1.25)
    # Customise the plot
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    ax.axhline(y=1, color="grey", linewidth=0.5, linestyle="--")
    # Set y-limits. We need to expand it by ~20% to make space for the legend,
    # as well as the averaged values.
    EXPANSION_FACTOR = 1.2
    ymin, ymax = ax.get_ylim()
    ymean = (ymin + ymax)/2
    ylength = (ymax - ymin)/2
    new_ymin = ymean - (EXPANSION_FACTOR * ylength)
    new_ymax = ymean + (EXPANSION_FACTOR * ylength)
    ax.set_ylim((new_ymin, new_ymax))
    # add the text
    for _, expt_avgs in avgd_ints.items():
        for i, ((_, avg), color) in enumerate(zip(expt_avgs.items(),
                                                  sns.color_palette("deep"))):
            ax.text(x=i, y=0.02, s=f"({avg:.2f})",
                    color=color, horizontalalignment="center",
                    transform=ax.get_xaxis_transform())
    pg.style_axes(ax, "plot")
    return plt.gcf(), ax

[g_ref_spv2, g_m_spv2, g_spv2_spv2] = [pg.read(g_path, expno) for expno in
                                       (4001, 12002, 42002)]
[z_ref_spv2, z_m_spv2, z_spv2_spv2] = [pg.read(z_path, expno) for expno in
                                       (4001, 12002, 42002)]

_, axs = pg.subplots(1, 2, figsize=(7, 4))
hsqc_stripplot(molecule=Grami,
               datasets=[g_m_spv2, g_spv2_spv2],
               ref_dataset=g_ref_spv2,
               expt_labels=["HMQC", "seHSQC"],
               xlabel=r"$^{15}$N module (with gramicidin)",
               ylabel=r"relative intensity of $^{13}$C seHSQC",
               ax=axs[0],
               loc="upper center")
hsqc_stripplot(molecule=Zolmi,
               datasets=[z_m_spv2, z_spv2_spv2],
               ref_dataset=z_ref_spv2,
               expt_labels=["HMQC", "seHSQC"],
               xlabel=r"$^{15}$N module (with zolmitriptan)",
               ylabel="",
               ax=axs[1],
               loc="upper center")
for ax in axs:
    ax.set_ylim(0.3, 1.2)
    pg.style_axes(ax, "plot")

pg.label_axes(axs, fontsize=14, fstr="({})", fontweight="bold")
# pg.show()
for filetype in [".png", ".svg"]:
    pg.savefig(str(Path(__file__)).replace(".py", filetype))
