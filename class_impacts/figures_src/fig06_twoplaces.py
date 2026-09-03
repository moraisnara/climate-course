"""
fig06_twoplaces — the picture the whole class turns on.

Two places, two daily-temperature distributions, and the same set of bin
cut-offs. A cold place spends real time in the bottom bin and never reaches the
top one; a hot place does the reverse.

In Dell, Jones & Olken (2014, Fig. 3) this figure is the SOLUTION: Phoenix
already lives in New York's future, so interacting weather with baseline
climate is a way to learn about adaptation. In Jones, Moscona, Olken & von
Dessauer (2026, Fig. 1) the same figure is the PROBLEM -- see fig07.

Schematic: Gaussian daily temperatures with the means and spreads of a
Boston-like and a Phoenix-like county. Not fitted data.
"""
import numpy as np
from scipy.stats import norm
import climstyle as cs

MU_COLD, MU_HOT, SIGMA = 50.0, 75.0, 17.0
EDGES = list(range(10, 100, 10))
x = np.linspace(-15, 120, 800)

fig, ax = cs.figure(cs.SIZE_WIDE)

for e in EDGES:
    ax.axvline(e, color=cs.GRID, linewidth=1.0, zorder=0)

ax.plot(x, norm.pdf(x, MU_COLD, SIGMA), color=cs.COOL, zorder=3)
ax.plot(x, norm.pdf(x, MU_HOT, SIGMA), color=cs.WARM, zorder=3)

xc = x[x <= 10]
ax.fill_between(xc, norm.pdf(xc, MU_COLD, SIGMA), color=cs.COOL, alpha=0.35, zorder=2)
xh = x[x >= 90]
ax.fill_between(xh, norm.pdf(xh, MU_HOT, SIGMA), color=cs.WARM, alpha=0.35, zorder=2)

ax.annotate("cold place\n(Boston)", xy=(MU_COLD, norm.pdf(MU_COLD, MU_COLD, SIGMA)),
            xytext=(-64, 6), textcoords="offset points", color=cs.COOL,
            fontsize=13, fontweight="bold", ha="center")
ax.annotate("hot place\n(Phoenix)", xy=(MU_HOT, norm.pdf(MU_HOT, MU_HOT, SIGMA)),
            xytext=(60, 6), textcoords="offset points", color=cs.WARM,
            fontsize=13, fontweight="bold", ha="center")
ax.annotate("$<$10$^\\circ$F", xy=(2, 0.0016), fontsize=12, color=cs.COOL,
            fontweight="bold", ha="center")
ax.annotate("$>$90$^\\circ$F", xy=(101, 0.0016), fontsize=12, color=cs.WARM,
            fontweight="bold", ha="center")

ax.set_yticks([])
ax.grid(False)
ax.set_xlim(-15, 122)
ax.set_ylim(0, 0.031)

cs.finish(ax,
          title="Daily temperature in two locations",
          subtitle="Daily temperature, schematic; bins every 10 $^\\circ$F",
          xlabel="Daily temperature ($^\\circ$F)",
          source="Schematic, after DJO (2014) Fig. 3 and JMOvD (2026) Fig. 1.")
cs.save(fig, "fig06_twoplaces")
