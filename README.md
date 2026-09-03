# Climate Course — two classes

Nara Morais · FEA/USP · 2026

Two guest classes for undergraduates. The first is conceptual (what climate does
to an economy, and how we could ever know); the second is an empirical
application of those concepts in R, with shapefiles and maps.

Decks are in **English**; the classes are taught in Portuguese.

## The two classes

**Class 1 — Climate Impacts.** Built on three papers that happen to form a
single arc:

1. Dell, Jones & Olken (2012), *AEJ: Macro* — "Temperature Shocks and Economic
   Growth." The workhorse panel design: within-country temperature fluctuations,
   country and year fixed effects. Growth, not just levels; poor countries only.
2. Dell, Jones & Olken (2014), *JEL* — "What Do We Learn from the Weather?" The
   method itself: weather vs. climate, what the panel design buys and what it
   costs, adaptation, and when a short-run estimate may be extrapolated.
3. Jones, Moscona, Olken & von Dessauer (2026), NBER w34671 — "With or Without
   U? Binning Bias and the Causal Effects of Temperature Extremes." The frontier
   pushing back on the standard nonlinear specification.

Same authors, 2012 → 2026: a design, its findings, and the design questioned
fourteen years later.

**Class 2 — Empirical Application.** The same concepts in R: daily maximum
temperature for every Brazilian municipality (BR-DWGD, via `brclimr`), 1961 and
2019, joined to IBGE boundaries with `geobr`. The class is built around one
question — *what is a hot day?* — and the fact that the answer moves the map.
Everything students run is `exercise/`.

## The decks

Both are Beamer, and both are committed compiled so you can read them without a
LaTeX install:

| Class | Source | Compiled |
|---|---|---|
| 1 — Climate Impacts | [`class_impacts/main.tex`](class_impacts/main.tex) | [`class_impacts/main.pdf`](class_impacts/main.pdf) — 35 frames, 42 pages |
| 2 — Empirical Application | [`class_empirics/main.tex`](class_empirics/main.tex) | [`class_empirics/main.pdf`](class_empirics/main.pdf) — 24 frames, 31 pages |

Every address on a slide is a live link, so the PDF works as the handout.

## The exercise

```
exercise/
  climate_data_in_R.R                        # the whole class, run top to bottom
  data/derived/tmax_daily_1961_2019.csv.gz   # 4,063,910 rows, 19.7 MB
```

Two files, on purpose. Section 2 of the script downloads the full 1.9 GB parquet
and rebuilds that CSV from it; every section after 2 reads the CSV instead, so a
clone runs in a couple of minutes without the download. Packages come from
`pacman::p_load()` at the top — `tidyverse`, `brclimr`, `arrow`, `geobr`, `sf`,
`glue`. Nothing else to source, nothing else to configure.

## Two toolchains, one palette

Class 1's figures are matplotlib (`class_impacts/figures_src/climstyle.py`),
which is the source of truth for the colours; they mirror `climatetheme.sty`
exactly, because a figure sitting on a slide in a near-but-not-quite teal reads
as a screenshot rather than part of the deck.

Class 2's figures are ggplot. `exercise/climate_data_in_R.R` deliberately does
**not** import a style file — it declares three colour vectors at the top of
section 4 and uses `theme_minimal()`. A teaching script that students clone
should have no dependency they have to go and find. The consequence is that the
plots a student gets are the deck's plots in ggplot's default furniture rather
than the house one, which is the right trade for a file that has to run on
someone else's laptop.

**`figures/` is generated; `figures_src/` is the truth.** Never hand-edit a file
in `class_impacts/figures/` — edit the script and rebuild, or the next build
silently reverts you. `class_empirics/figures/` holds the two screenshots and
the three plots the exercise script writes itself.

## Building a deck

```bash
cd class_impacts
python figures_src/build_all.py          # regenerate figures/
pdflatex main.tex && pdflatex main.tex   # twice, for section navigation
```
