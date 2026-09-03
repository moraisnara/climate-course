"""
fig01_variation — what the fixed effects cost you.

Dell, Jones & Olken (2012), Table 1: the proportion of country-years whose
temperature is at least 1.00 C away from that country's own mean, before and
after the fixed effects that buy identification.

The point of the slide: identification is not free. Two thirds of the usable
variation is gone by the time the design is credible.
"""
import climstyle as cs

LABELS = ["Raw\ndeviations",
          "+ worldwide\nyear FE",
          "+ region$\\times$year and\npoor$\\times$year FE"]
VALUES = [0.064, 0.032, 0.018]

fig, ax = cs.figure(cs.SIZE)
bars = ax.bar(LABELS, VALUES, color=[cs.SEQ[0], cs.SEQ[1], cs.BRAND], width=0.62)

for b, v in zip(bars, VALUES):
    ax.annotate(f"{v:.3f}", xy=(b.get_x() + b.get_width() / 2, v),
                xytext=(0, 5), textcoords="offset points",
                ha="center", fontsize=14, fontweight="bold", color=cs.INK)

ax.set_ylim(0, 0.078)
ax.set_yticks([0, 0.02, 0.04, 0.06])
ax.tick_params(axis="x", labelsize=12)

cs.finish(ax,
          title="Temperature variation after fixed effects",
          subtitle="Share of country-years $\\geq$ 1 $^\\circ$C from the country mean",
          source="Dell, Jones & Olken (2012), AEJ: Macro, Table 1. 1950-2003.")
cs.save(fig, "fig01_variation")
