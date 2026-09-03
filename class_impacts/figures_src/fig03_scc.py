"""
fig03_scc — the social cost of carbon is a discount rate in disguise.

Weitzman's calibration of the same damage stream at three discount rates
($1 at 7%, $21 at 3%, $266 at 1%), with the Nordhaus and Stern headline
numbers plotted at the rates each of them used.

The slide's claim: Stern and Nordhaus do not disagree about the climate. They
disagree about r, and the SCC is exponentially sensitive to it.
"""
import numpy as np
import climstyle as cs

RATES = np.array([7.0, 3.0, 1.0])
SCC = np.array([1.0, 21.0, 266.0])

fig, ax = cs.figure(cs.SIZE)
ax.plot(RATES, SCC, color=cs.BRAND, marker="o", markersize=9, zorder=3)

for r, v in zip(RATES, SCC):
    ax.annotate(f"\\${v:.0f}", xy=(r, v), xytext=(0, 12), textcoords="offset points",
                ha="center", fontsize=14, fontweight="bold", color=cs.BRAND)

ax.scatter([5.5], [20], s=130, color=cs.ACCENT, marker="D", zorder=4)
ax.annotate("Nordhaus\n$\\sim$\\$20 at 5.5%", xy=(5.5, 20), xytext=(0, 16),
            textcoords="offset points", ha="center", fontsize=12,
            color=cs.ACCENT, fontweight="bold")
ax.scatter([1.4], [200], s=130, color=cs.WARM, marker="D", zorder=4)
ax.annotate("Stern\n\\$200+ at 1.4%", xy=(1.4, 200), xytext=(24, -44),
            textcoords="offset points", ha="center", fontsize=12,
            color=cs.WARM, fontweight="bold")

ax.set_yscale("log")
ax.set_xlim(7.8, 0.2)
ax.set_ylim(0.6, 900)
ax.set_yticks([1, 10, 100])
ax.set_yticklabels(["\\$1", "\\$10", "\\$100"])

cs.finish(ax,
          title="Social cost of carbon by discount rate",
          subtitle="Social cost of carbon, \\$ per ton of CO$_2$ (log scale)",
          xlabel="Discount rate (%)",
          source="Weitzman calibration, in Dell, Jones & Olken (2014), Sec. 4.2.")
cs.save(fig, "fig03_scc")
