"""
fig08_taxonomy — Result 2 of Jones, Moscona, Olken & von Dessauer (2026).

Write the place-specific outcome trend as lambda_i = a_Y + b_Y * T_0i + e_i:
the trend in the outcome is allowed to depend on how hot the place was to
begin with. Then the sign of b_Y alone decides the shape of the spurious
pattern in the estimated bin coefficients:

    b_Y > 0  ->  spurious U
    b_Y < 0  ->  spurious inverted U
    b_Y = 0  ->  no bias

Schematic of the theoretical result: the true effect of every bin is zero in
all three panels.
"""
import numpy as np
import matplotlib.pyplot as plt
import climstyle as cs

BINS = np.arange(-4, 5)
SHAPE = 0.028 * BINS ** 2 - 0.11

PANELS = [("$b_Y > 0$", "spurious U", SHAPE, cs.WARM),
          ("$b_Y < 0$", "spurious inverted U", -SHAPE, cs.COOL),
          ("$b_Y = 0$", "no bias", np.zeros_like(SHAPE), cs.MUTED)]

fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.4), sharey=True)

for ax, (cond, name, beta, color) in zip(axes, PANELS):
    ax.axhline(0, color=cs.MUTED, linewidth=1.0, linestyle="--", zorder=1)
    ax.plot(BINS, beta, color=color, marker="o", markersize=6, zorder=3)
    ax.set_title(f"{cond}\n{name}", fontsize=13, color=cs.INK, pad=8)
    ax.set_xticks([BINS[0], 0, BINS[-1]])
    ax.set_xticklabels(["cold", "mild", "hot"], fontsize=12)
    ax.set_ylim(-0.52, 0.52)
    ax.grid(axis="y", visible=True)

axes[0].set_ylabel("$\\hat{\\beta}_k$", color=cs.MUTED, fontsize=13)
for ax in axes:
    ax.tick_params(length=0)

fig.suptitle("Bias in the estimated bin coefficients", x=0.005, ha="left",
             fontsize=15, fontweight="bold", color=cs.INK)
fig.text(0.005, 0.020,
         "Schematic of Result 2 in Jones, Moscona, Olken & von Dessauer (2026); the true effect of every bin is zero.",
         fontsize=9, color=cs.MUTED, ha="left", va="bottom")

cs.save(fig, "fig08_taxonomy")
