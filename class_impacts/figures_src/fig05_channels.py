"""
fig05_channels — it is not only agriculture.

Dell, Jones & Olken (2012), Tables 2 and 5: the growth effect of +1 C in poor
countries, for aggregate output and for its components.

The slide's claim: industry moves almost as much as agriculture, which rules
out "this is a story about farms" and is why the effect looks like growth.
"""
import climstyle as cs

ROWS = [("Aggregate\nGDP growth", -1.39, "***"),
        ("Agricultural\nvalue added", -2.66, "***"),
        ("Industrial\nvalue added", -2.04, "**")]

fig, ax = cs.figure(cs.SIZE)
bars = ax.bar([r[0] for r in ROWS], [r[1] for r in ROWS],
              color=[cs.BRAND, cs.SEQ[1], cs.ACCENT], width=0.58)
ax.axhline(0, color=cs.MUTED, linewidth=1.0)

for b, (_, v, stars) in zip(bars, ROWS):
    ax.annotate(f"{v:.2f}{stars}", xy=(b.get_x() + b.get_width() / 2, v),
                xytext=(0, 22), textcoords="offset points",
                ha="center", fontsize=14, fontweight="bold", color="white")

ax.set_ylim(-3.15, 0.35)
ax.tick_params(axis="x", labelsize=12)

cs.finish(ax,
          title="Effect of temperature by sector",
          subtitle="Effect of +1 $^\\circ$C in poor countries, pp of growth",
          source="Dell, Jones & Olken (2012), Tables 2 and 5. Rich countries: zero.")
cs.save(fig, "fig05_channels")
