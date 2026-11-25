"""Typography, colors and export settings for the benchmark figures."""

from pathlib import Path


INK = "#182738"
MUTED = "#45586D"
GRID = "#E0E8F0"
BASELINE = "#63748B"
MTP = "#215BC0"
DSPARK = "#087F72"
DFLASH = "#AF471D"
PLUM = "#764DA2"


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
        "legend.fontsize": 9.75,
        "legend.frameon": False,
        "legend.handlelength": 2.1,
        "lines.linewidth": 2,
        "lines.markersize": 5.5,
        "text.color": INK,
        "savefig.facecolor": "white",
        "svg.fonttype": "path",
        "svg.hashsalt": "speculative-decoding-report",
    })
    return plt


def save_plot(fig, plt, output, name):
    fig.savefig(output / f"{name}.png", dpi=180, bbox_inches="tight", pad_inches=0.13)
    svg = output / f"{name}.svg"
    fig.savefig(svg, bbox_inches="tight", pad_inches=0.13, metadata={"Date": None})
    contents = svg.read_text(encoding="utf-8").splitlines()
    svg.write_text("\n".join(line.rstrip() for line in contents) + "\n", encoding="utf-8")
    plt.close(fig)
