"""Typography, colors and export settings for the benchmark figures."""

from pathlib import Path


INK = "#182738"
MUTED = "#45586D"
GRID = "#E2E7EF"
BASELINE = "#63748B"
DFLASH = "#C94F00"
SUFFIX = "#A64477"
METHOD_STYLES = {
    "mtp": ("#0072B2", "o", "-"),
    "dspark": ("#087B60", "s", "--"),
    "dflash": (DFLASH, "D", "-."),
    "eagle4": ("#454184", "^", "-"),
    "suffix": (SUFFIX, "P", "--"),
}


def setup_plots():
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import font_manager
    import matplotlib.pyplot as plt

    fonts = Path(__file__).resolve().parents[1] / "assets" / "fonts"
    for weight in ("Regular", "Semibold"):
        font_manager.fontManager.addfont(fonts / f"SourceSans3-{weight}.ttf")

    plt.rcParams.update({
        "font.family": "Source Sans 3",
        "font.size": 11,
        "figure.facecolor": "white",
        "figure.dpi": 120,
        "axes.labelsize": 10.5,
        "axes.labelcolor": MUTED,
        "axes.titlesize": 12,
        "axes.titleweight": "semibold",
        "axes.titlecolor": INK,
        "axes.edgecolor": "#C3D1DF",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.major.size": 3,
        "ytick.major.size": 0,
        "axes.formatter.use_locale": False,
        "xtick.labelsize": 10.25,
        "ytick.labelsize": 10.25,
        "legend.fontsize": 10,
        "legend.frameon": False,
        "legend.handlelength": 2.1,
        "lines.linewidth": 1.85,
        "lines.markersize": 6.4,
        "text.color": INK,
        "savefig.facecolor": "white",
        "pdf.fonttype": 42,
        "svg.fonttype": "path",
        "svg.hashsalt": "speculative-decoding-report",
    })
    return plt


def save_plot(fig, plt, output, name):
    fig.savefig(output / f"{name}.png", dpi=300, bbox_inches="tight", pad_inches=0.13)
    fig.savefig(output / f"{name}.pdf", bbox_inches="tight", pad_inches=0.13,
                metadata={"CreationDate": None, "ModDate": None})
    svg = output / f"{name}.svg"
    fig.savefig(svg, bbox_inches="tight", pad_inches=0.13, metadata={"Date": None})
    contents = svg.read_text(encoding="utf-8").splitlines()
    svg.write_text("\n".join(line.rstrip() for line in contents) + "\n", encoding="utf-8")
    plt.close(fig)
