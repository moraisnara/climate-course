"""
fig07_binshift — where binning bias comes from, derived rather than asserted.

Take the schematic distributions of fig06 and warm every place by the same
+2 F. The CHANGE in days spent in each extreme bin is not the same everywhere:
it depends on where the place started.

    days below 10F  = 365 * Phi((10 - mu)/sigma)
    days above 90F  = 365 * (1 - Phi((90 - mu)/sigma))

Differentiating in mu, both changes are increasing in baseline temperature.
That is exactly the empirical pattern in Jones, Moscona, Olken & von Dessauer
(2026), Fig. 3, across US counties -- and it is a mechanical consequence of
uniform warming, not a fact about any economy.

If a place's OUTCOME also trends with its baseline temperature, for any
reason, the panel regression attributes that trend to the extreme bins.
"""
import numpy as np
from scipy.stats import norm
import climstyle as cs

SIGMA, WARMING = 17.0, 2.0
mu = np.linspace(35, 80, 400)

cold_days = lambda m: 365 * norm.cdf((10 - m) / SIGMA)
hot_days = lambda m: 365 * (1 - norm.cdf((90 - m) / SIGMA))

d_cold = cold_days(mu + WARMING) - cold_days(mu)
d_hot = hot_days(mu + WARMING) - hot_days(mu)

fig, ax = cs.figure(cs.SIZE)
ax.axhline(0, color=cs.MUTED, linewidth=1.0, zorder=1)
ax.plot(mu, d_cold, color=cs.COOL, zorder=3)
ax.plot(mu, d_hot, color=cs.WARM, zorder=3)

ax.set_xlim(35, 80)
ax.set_ylim(-11, 17)

ax.text(43.5, 11.5, "$\\Delta$ days $>$ 90$^\\circ$F",
        color=cs.WARM, fontsize=13, fontweight="bold")
ax.text(56.5, -6.6, "$\\Delta$ days $<$ 10$^\\circ$F",
        color=cs.COOL, fontsize=13, fontweight="bold")

for m, name in [(50, "Boston"), (75, "Phoenix")]:
    ax.axvline(m, color=cs.GRID, linewidth=1.4, zorder=0)
    ax.annotate(name, xy=(m, -9.6), fontsize=12, color=cs.MUTED,
                ha="center", style="italic")

cs.finish(ax,
          title="Change in exposure to the extreme bins",
          subtitle="Change in days per year, after a uniform +2 $^\\circ$F",
          xlabel="Baseline mean daily temperature ($^\\circ$F)",
          source="Derived from fig06. Empirical counterpart: JMOvD (2026), Fig. 3.")
cs.save(fig, "fig07_binshift")
