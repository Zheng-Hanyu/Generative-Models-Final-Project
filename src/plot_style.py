"""Shared palette, typography and high-resolution export for benchmark figures."""

from statistics import median


INK = "#171D27"
MUTED = "#45505D"
GRID = "#E3E7EB"
BASELINE = "#65717D"
DFLASH = "#BE560F"
SUFFIX = "#A84578"
METHOD_STYLES = {
    "mtp": ("#0072B2", "o", "-"),
    "dspark": ("#087B61", "s", "--"),
    "dflash": (DFLASH, "D", "-."),
    "eagle4": ("#5145A1", "^", "-"),
    "suffix": (SUFFIX, "P", "--"),
    "suffix-standard": ("#695630", "v", ":"),
}
BAR_HATCHES = {"mtp": "", "dspark": "//", "dflash": ".", "eagle4": "", "suffix": "\\\\"}


def setup_plots():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties, findfont

    family = "TeX Gyre Pagella"
    try:
        regular = findfont(FontProperties(family=family, weight="normal"), fallback_to_default=False)
        bold = findfont(FontProperties(family=family, weight="bold"), fallback_to_default=False)
    except ValueError as error:
        raise ValueError("Install TeX Gyre Pagella (Regular and Bold) to render report figures") from error
    if regular == bold:
        raise ValueError("Install both TeX Gyre Pagella Regular and Bold to render report figures")

    plt.rcParams.update({
        "font.family": family,
        "font.size": 10,
        "axes.labelsize": 10,
        "axes.labelcolor": INK,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.titlecolor": INK,
        "axes.edgecolor": "#A4ADB6",
        "axes.linewidth": 0.75,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.65,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "axes.formatter.use_locale": False,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 9.5,
        "legend.frameon": False,
        "legend.handlelength": 2.15,
        "lines.linewidth": 1.7,
        "lines.markersize": 5.8,
        "text.color": INK,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    })
    return plt


def speed_bars(ax, groups):
    """Draw paired medians and observed ranges for one workload."""
    methods = list(groups)
    concurrencies = list(groups[methods[0]])
    width = min(0.52, 0.72 / len(methods))
    peak = 1.0
    ax.grid(axis="y")
    ax.axhline(1, color=BASELINE, linestyle="--", linewidth=1.0, zorder=3)
    for index, method in enumerate(methods):
        color, _, _ = METHOD_STYLES[method]
        samples = [groups[method][c] for c in concurrencies]
        centers = [median(runs) for runs in samples]
        positions = [i + (index - (len(methods) - 1) / 2) * width for i in range(len(samples))]
        ax.bar(positions, centers, width=width * 0.88, color=color, edgecolor="#FFFFFF",
               linewidth=0.5, hatch=BAR_HATCHES[method], label=method, zorder=2)
        error = [(x, center, center - min(runs), max(runs) - center)
                 for x, center, runs in zip(positions, centers, samples, strict=True) if len(runs) > 1]
        if error:
            xs, ys, lower, upper = zip(*error)
            ax.errorbar(xs, ys, yerr=(lower, upper),
                        fmt="none", capsize=2.3, color=INK, linewidth=0.9, zorder=4)
        peak = max(peak, max(max(runs) for runs in samples))
    ax.set_xticks(range(len(concurrencies)), concurrencies)
    ax.set_xlim(-0.55, len(concurrencies) - 0.45)
    return peak


def save_plot(fig, plt, output, name):
    fig.savefig(output / f"{name}.png", dpi=400, bbox_inches="tight", pad_inches=0.13)
    plt.close(fig)
