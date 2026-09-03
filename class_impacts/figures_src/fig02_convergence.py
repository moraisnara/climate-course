"""
fig02_convergence — independent literatures, one number.

Estimates surveyed in Dell, Jones & Olken (2014, JEL, Section 3): losses of
roughly 1-2 percent per +1 C, arrived at from aggregate growth regressions,
industrial value added, exports, and micro labour-productivity studies that
share neither data nor method.

The slide's claim: the convergence is the evidence, not any single paper.
"""
import climstyle as cs

# (label, point estimate in % per +1 C, which literature)
ROWS = [
    ("Call centres (Niemela et al. 2002)",        1.8, "micro"),
    ("Labour, hot days (Seppanen et al. 2006)",   2.0, "micro"),
    ("Industry, poor (DJO 2012)",                 2.0, "macro"),
    ("Manufacturing (Hsiang 2010)",               2.4, "macro"),
    ("Exports, poor (Jones & Olken 2010)",        2.4, "macro"),
    ("Caribbean output (Hsiang 2010)",            2.5, "macro"),
    ("GDP growth, poor (DJO 2012)",               1.4, "macro"),
]

fig, ax = cs.figure((6.4, 3.9))
ys = range(len(ROWS))
colors = [cs.ACCENT if r[2] == "micro" else cs.BRAND for r in ROWS]
ax.scatter([r[1] for r in ROWS], list(ys), s=110, color=colors, zorder=3)
ax.hlines(list(ys), 0, [r[1] for r in ROWS], color=cs.GRID, linewidth=6, zorder=1)

ax.axvspan(1.0, 2.5, color=cs.BRAND, alpha=0.07, zorder=0)
ax.set_yticks(list(ys))
ax.set_yticklabels([r[0] for r in ROWS], fontsize=12)
ax.set_xlim(0, 2.9)
ax.grid(axis="y", visible=False)
ax.grid(axis="x", visible=True)
ax.invert_yaxis()

cs.finish(ax,
          title="Estimates across the literature",
          subtitle="Micro studies in orange, macro studies in teal",
          xlabel="% loss per +1 $^\\circ$C",
          source="Surveyed in Dell, Jones & Olken (2014), JEL, Sec. 3.")
cs.save(fig, "fig02_convergence")
