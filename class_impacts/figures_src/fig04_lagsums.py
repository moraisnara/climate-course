"""
fig04_lagsums — the single test that separates a level effect from a growth effect.

Dell, Jones & Olken (2012), Table 3: the cumulative sum of the temperature
coefficients in poor countries as lags are added to equation (4).

If temperature only moved the LEVEL of output, the distributed lag would
undo itself and the sum would walk back to zero. It does not.
"""
import climstyle as cs

LAGS = [0, 1, 5, 10]
NO_PRECIP = [-1.394, -1.096, -1.235, -1.171]
WITH_PRECIP = [-1.347, -0.983, -1.041, -0.858]

fig, ax = cs.figure(cs.SIZE)
ax.axhline(0, color=cs.MUTED, linewidth=1.4, linestyle="--", zorder=1)
ax.plot(LAGS, NO_PRECIP, color=cs.ACCENT, marker="o", markersize=8, zorder=3)
ax.plot(LAGS, WITH_PRECIP, color=cs.BRAND, marker="s", markersize=8, zorder=3)

ax.annotate("temperature only", xy=(5, NO_PRECIP[2]), xytext=(0, -26),
            textcoords="offset points", ha="center", color=cs.ACCENT,
            fontsize=13, fontweight="bold")
ax.annotate("+ precipitation", xy=(5, WITH_PRECIP[2]), xytext=(0, 12),
            textcoords="offset points", ha="center", color=cs.BRAND,
            fontsize=13, fontweight="bold")

ax.annotate("a pure level effect\nwould return here",
            xy=(7.6, 0), xytext=(0, 10), textcoords="offset points",
            ha="center", fontsize=12, color=cs.MUTED, style="italic")

ax.set_xticks(LAGS)
ax.set_ylim(-1.75, 0.55)
ax.set_xlim(-0.6, 10.9)

cs.finish(ax,
          title="Cumulative effect of lagged temperature",
          subtitle="Cumulative $\\rho_j$, poor countries, pp per $^\\circ$C",
          xlabel="Number of lags $L$ in equation (4)",
          source="Dell, Jones & Olken (2012), Table 3. Rich countries: 0 throughout.")
cs.save(fig, "fig04_lagsums")
