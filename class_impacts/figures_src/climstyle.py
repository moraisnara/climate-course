"""
climstyle.py  --  Shared house style for all Class 1 figures.

One import gives every figure the same fonts, colors, weights and spacing, so
the deck reads as a single designed system instead of screenshots from many
sources. Palette is colorblind-safe and validated (see valpal / dataviz method):
categorical gases separate under protan/deutan/tritan; data marks clear the
OKLCH lightness band and chroma floor.

Usage
-----
    import climstyle as cs
    fig, ax = cs.figure()          # styled figure + axis
    ax.plot(x, y, color=cs.CO2)
    cs.finish(ax, title="...", source="Source: ...")
    cs.save(fig, "fig01_temperature")   # writes ../figures/<name>.pdf and .png
"""
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager

# --------------------------------------------------------------------------
# Palette (validated, colorblind-safe). Frame furniture uses the deck brand;
# data marks use tuned steps that clear the chroma floor / contrast checks.
# --------------------------------------------------------------------------
BRAND   = "#005F73"   # deck teal — titles, rules, non-data furniture
INK     = "#14213D"   # near-black navy — primary text
MUTED   = "#6C757D"   # secondary text, captions, source lines
GRID    = "#E9ECEF"   # recessive gridlines
SURFACE = "#FCFCFB"   # chart surface (matches validator light surface)

# Categorical — greenhouse gases (fixed order, never cycled)
CO2 = "#00809B"       # teal, tuned up in chroma from the brand
CH4 = "#CA6702"       # deck orange
N2O = "#E9A100"       # gold
GASES = [CO2, CH4, N2O]

# Single-series / accent
ACCENT  = "#CA6702"   # orange — the "one line that matters"
NEUTRAL = "#6C757D"   # grey series / reference lines

# Sequential ramp (ordered magnitude, e.g. income groups) light -> dark
SEQ = ["#7FBECD", "#3E97AC", "#0A7387", "#004E5F"]

# Warming stripe / diverging poles (cool -> warm), neutral midpoint = SURFACE
COOL = "#08519C"
WARM = "#B2182B"

# --------------------------------------------------------------------------
# Fonts. Prefer a clean humanist sans if present; fall back gracefully.
# --------------------------------------------------------------------------
_PREFERRED = ["Source Sans 3", "Source Sans Pro", "Segoe UI", "Arial",
              "Helvetica", "DejaVu Sans"]
_available = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((f for f in _PREFERRED if f in _available), "DejaVu Sans")

mpl.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "figure.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "font.family": FONT,
    "font.size": 15,
    "text.color": INK,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "axes.titlecolor": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "xtick.labelcolor": INK,
    "ytick.labelcolor": INK,
    "axes.linewidth": 0.8,
    "axes.grid": True,
    "axes.grid.axis": "y",
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "lines.linewidth": 2.2,
    "lines.solid_capstyle": "round",
    "legend.frameon": False,
    "legend.fontsize": 14,
    "figure.constrained_layout.use": True,
})

# Figure sizes (inches) are set to the ON-SLIDE display size, NOT an arbitrary
# large canvas. In a two-column frame a 0.5\linewidth column is ~2.76 in wide at
# aspectratio=169; a figure placed there with width=\linewidth is scaled DOWN by
# includegraphics, and that scale applies to text and plot together. Generating
# near display width (a mild ~0.5x down-scale) keeps label text legible on the
# slide (~8-10 pt effective) instead of the ~4-5 pt a 9 in canvas produced.
#   SIZE       -> a single column of a two-column frame (~0.5 width)
#   SIZE_WIDE  -> a slightly wider single column (~0.56) or a full-width band
#   SIZE_SQUARE-> square-ish single column (schematics, tile grids)
# Height-constrained centered figures (includegraphics height=...) set their own
# size so that display_height/native_height gives the same ~0.5 down-scale.
SIZE = (5.2, 3.7)
SIZE_WIDE = (5.8, 3.5)
SIZE_SQUARE = (4.9, 4.2)

FIGDIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "..", "figures"))


def figure(size=SIZE):
    """A styled figure + single axis."""
    fig, ax = plt.subplots(figsize=size)
    return fig, ax


def finish(ax, title=None, subtitle=None, ylabel=None, xlabel=None, source=None):
    """Apply the shared title block, axis labels and source line."""
    # Furniture (title / subtitle / source) is sized for the ~half-column canvas:
    # the deck's teal frame title already carries the headline, so the chart
    # title is secondary and kept compact so it does not overrun the narrow
    # canvas. Data labels (ticks, direct labels, callouts) stay large — those are
    # what must read from the back of the hall.
    if title:
        ax.set_title(title, loc="left", fontsize=15, fontweight="bold",
                     color=INK, pad=22 if subtitle else 10)
    if subtitle:
        ax.text(0.0, 1.02, subtitle, transform=ax.transAxes, fontsize=12,
                color=MUTED, ha="left", va="bottom")
    if ylabel:
        ax.set_ylabel(ylabel, color=MUTED, fontsize=13)
    if xlabel:
        ax.set_xlabel(xlabel, color=MUTED, fontsize=13)
    ax.tick_params(length=0)
    if source:
        ax.figure.text(0.01, 0.018, source, ha="left", va="bottom",
                        fontsize=9, color=MUTED)


def label_end(ax, x, y, text, color, dx=6, dy=0, **kw):
    """Direct end-of-line label (replaces a legend for the key series)."""
    ax.annotate(text, xy=(x, y), xytext=(dx, dy), textcoords="offset points",
                color=color, fontsize=14, fontweight="bold", va="center", **kw)


def save(fig, name):
    """Write both PDF (for LaTeX) and PNG (for quick preview) into figures/."""
    # Reserve a bottom strip (and small margins) so the source caption placed by
    # finish()/scripts via fig.text doesn't collide with the x-axis. constrained
    # layout otherwise ignores figure-level text.
    eng = fig.get_layout_engine()
    if eng is not None:
        try:
            eng.set(rect=(0.006, 0.065, 0.988, 0.85))
        except Exception:
            pass
    os.makedirs(FIGDIR, exist_ok=True)
    pdf = os.path.join(FIGDIR, name + ".pdf")
    png = os.path.join(FIGDIR, name + ".png")
    fig.savefig(pdf)
    fig.savefig(png)
    plt.close(fig)
    print(f"  wrote {os.path.relpath(pdf, os.getcwd())}")
    return pdf
