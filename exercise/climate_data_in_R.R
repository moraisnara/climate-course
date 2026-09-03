# =============================================================================
#  Climate data in R
#  Climate Course -- FEA/USP -- Class
#  Nara Morais
# =============================================================================
# 1. Preambulo -----------------------------------------------------------------
# In here, put the R packages that we need to load
if (!requireNamespace("pacman", quietly = TRUE)) install.packages("pacman")

pacman::p_load(
  tidyverse,    # dplyr, ggplot2, tidyr, lubridate... the verbs we use all day
  brclimr,      # Brazilian municipal climate data, already aggregated
  arrow,        # reads parquet, and lets dplyr verbs run inside the file
  geobr,        # official IBGE boundaries -- the shapefiles
  sf,           # how R holds a map: a data frame with a geometry column
  glue          # string interpolation, for readable plot labels
)

# 2. The data ------------------------------------------------------------------

# 2.1 One municipality, one call -----------------------------------------------

sp_2019 <- brclimr::fetch_data(
  code_muni  = 3550308,              # Sao Paulo
  product    = "brdwgd",             # BR-DWGD
  indicator  = "tmax",               # daily maximum temperature
  statistics = "mean",               # <- read the note below
  date_start = as.Date("2019-01-01"),
  date_end   = as.Date("2019-12-31")
)

dim(sp_2019)      
head(sp_2019)

# 2.2 Whole country -----------------------------------------------------------

# fetch_data() takes ONE municipality per call. For the whole country we skip
# the package and go to the file it reads: one parquet, every municipality,
# 1961 to July 2020.

# --- 2.2.1 Download it once, then read it with arrow -------------------------

tmax_url     <- brclimr::brdwgd_data$tmax$link
tmax_bytes   <- 1934412877           # the server's Content-Length
tmax_parquet <- file.path(tools::R_user_dir("climate-course", "cache"),
                          "brdwgd_tmax.parquet")


dir.create(dirname(tmax_parquet), recursive = TRUE, showWarnings = FALSE)

if (!file.exists(tmax_parquet) || file.size(tmax_parquet) != tmax_bytes) {
  options(timeout = 3600)      # the default 60 seconds will not survive 1.9 GB
  download.file(tmax_url, tmax_parquet, mode = "wb")
}

brdwgd <- arrow::open_dataset(tmax_parquet)

tmax_daily <- brdwgd |>
  filter(name == "Tmax_mean",
         (date >= as.Date("1961-01-01") & date <= as.Date("1961-12-31")) |
         (date >= as.Date("2019-01-01") & date <= as.Date("2019-12-31"))) |>
  mutate(year = year(date)) |>
  select(code_muni, year, date, value) |>
  collect() |>
  arrange(code_muni, date) |>
  mutate(value = round(value, 2))

dir.create("data/derived", recursive = TRUE, showWarnings = FALSE)
write_csv(tmax_daily, "data/derived/tmax_daily_1961_2019.csv.gz")     # 19.7 MB

# None of these build the file -- they are here to look at in class.
brclimr::brdwgd_data$tmax$date_range   # "Daily, 1961-01-01 to 2020-07-31"
brclimr::brdwgd_data$tmax$stats        # mean -> "Tmax_mean", sd -> "Tmax_sd", ...
brdwgd                                 # the schema
nrow(brdwgd)                           # 484,596,216 rows, none of them in memory
dim(tmax_daily)                        # 4,063,910 x 4
count(tmax_daily, year)                # 2,031,955 each -- 5,567 munis x 365 days



# 3. Some descriptives ---------------------------------------------------------

tmax_daily <- read.csv("data/derived/tmax_daily_1961_2019.csv.gz")

tmax_yearly <- tmax_daily %>% 
  group_by(code_muni, year) %>% 
  summarise(n_days    = n(),
            mean_temp = mean(value, na.rm = TRUE),
            median_temp = median(value, na.rm = TRUE),
            max_temp  = max(value, na.rm = TRUE),
            min_temp  = min(value, na.rm = TRUE),
            .groups   = "drop") %>% 
  arrange(year)

# Joining with geodata

muni <- geobr::read_municipality(
  code_muni = "all", year = 2010,
  simplified = TRUE, showProgress = FALSE
)

muni <- muni %>% 
  select(code_muni, name_muni, abbrev_state, name_region)

tmax_yearly <- muni %>% 
  left_join(tmax_yearly, by = "code_muni")

# What is a hot temperature?

stat <- tmax_yearly %>%
  sf::st_drop_geometry() %>% 
  group_by(year) %>% 
  summarise(mean_t = mean(max_temp, na.rm = TRUE),
            max_t  = max(max_temp, na.rm = TRUE),
            min_t  = min(max_temp,  na.rm = TRUE),
            .groups   = "drop")
stat


# 3.2 What is a hot day? -------------------------------------------------------

# A hot day is a day above a threshold. Nothing tells us where the threshold is,
# so we have to pick one. Three candidates, all of them "the mean" -- they just
# disagree about the mean of WHAT.

geo   <- muni %>% sf::st_drop_geometry()
daily <- tmax_daily %>% left_join(geo, by = "code_muni")

ref_br <- daily %>%
  group_by(year) %>%
  summarise(ref_br = mean(value, na.rm = TRUE), .groups = "drop")

ref_region <- daily %>%
  group_by(year, name_region) %>%
  summarise(ref_region = mean(value, na.rm = TRUE), .groups = "drop")

ref_state <- daily %>%
  group_by(year, abbrev_state) %>%
  summarise(ref_state = mean(value, na.rm = TRUE), .groups = "drop")

ref_br
ref_region %>% pivot_wider(names_from = year, values_from = ref_region)
ref_state  %>% pivot_wider(names_from = year, values_from = ref_state) %>% arrange(`2019`)

# One threshold for Brazil, five for the regions, twenty-seven for the states --
# plus 30 C, which comes from nowhere in the data at all.

hot <- daily %>%
  left_join(ref_br,     by = "year") %>%
  left_join(ref_region, by = c("year", "name_region")) %>%
  left_join(ref_state,  by = c("year", "abbrev_state")) %>%
  group_by(code_muni, name_muni, abbrev_state, name_region, year) %>%
  summarise(mean_temp  = mean(value),
            hot_br     = sum(value > ref_br),
            hot_region = sum(value > ref_region),
            hot_state  = sum(value > ref_state),
            hot_30     = sum(value >= 30),
            .groups    = "drop")

# No na.rm here on purpose: the 9 municipalities with no data come out NA
# instead of 0, which is what they are.
hot %>% filter(is.na(hot_br)) %>% count(year)

hot %>%
  group_by(year) %>%
  summarise(across(starts_with("hot_"), ~ mean(.x, na.rm = TRUE)))

CITIES <- c(1302603, 2211001, 5300108, 3550308, 4106902)

hot %>%
  filter(year == 2019, code_muni %in% CITIES) %>%
  select(name_muni, abbrev_state, mean_temp, hot_br, hot_region, hot_state, hot_30) %>%
  arrange(mean_temp)

# Same municipality, same year, four answers. Teresina is 360 days above 30 C
# and about half that above its own state's mean: the state reference cannot
# say Piaui is hot, because Piaui is what it divided by.

# The deck says 359, not 360. Both are right -- the parquet is 25/03/2019 at
# 29.9967, and rounding to two decimals moves it across.
daily %>% filter(code_muni == 2211001, year == 2019, value == 30) %>% select(date, value)


# 4. Maps ----------------------------------------------------------------------

# Our own colours instead of ggplot's defaults. Nothing to install, nothing to
# source -- change the hex codes and every figure below follows.
#
# SEQ runs cool -> sand -> hot rather than through one hue: on a 0-365 scale a
# single-hue ramp puts most municipalities in the same mid-tone, and the two
# maps below stop being distinguishable. Sand sits at roughly half the year.

PAL <- c("#00809B", "#CA6702")                          # two categories
SEQ <- c("#005F73", "#0A9396", "#94D2BD",               # low  -> cool
         "#E9D8A6",                                     #      -> middle
         "#EE9B00", "#CA6702", "#9B2226")               # high -> hot
INK <- "#14213D"

dir.create("figures", showWarnings = FALSE)

uf <- geobr::read_state(year = 2010, simplified = TRUE, showProgress = FALSE)

map_df <- muni %>%
  left_join(hot %>% filter(year == 2019) %>% select(code_muni, hot_br, hot_state),
            by = "code_muni") %>%
  pivot_longer(c(hot_br, hot_state), names_to = "measure", values_to = "n_hot") %>%
  mutate(measure = factor(measure, c("hot_br", "hot_state"),
                          c("Above the national mean",
                            "Above its own state's mean")))

fig12 <- ggplot(map_df) +
  geom_sf(aes(fill = n_hot), colour = NA) +
  geom_sf(data = uf, fill = NA, colour = "white", linewidth = 0.15) +
  facet_wrap(~ measure) +
  scale_fill_gradientn(colours = SEQ, limits = c(0, 365), na.value = "grey90") +
  coord_sf(xlim = c(-74.1, -34.7), ylim = c(-33.8, 5.4)) +
  labs(title = "Hot days in 2019 -- the same data, two references",
       fill = "days") +
  theme_void()

fig12

# png, not pdf: 5,565 polygons as vector art is a multi-megabyte file.
ggsave("figures/fig12_hot_reference.png", fig12,
       width = 5.6, height = 3.4, dpi = 300, bg = "white")

# Same scale, same year, same municipalities. The left map is Brazil's climate.
# On the right the state borders show up in the data itself, because every
# municipality is being compared with the state it sits in -- the North stops
# looking hot and the South stops looking cold.
# Swap hot_state for hot_30 above to see the absolute threshold instead.


# 5. The two distribution figures ----------------------------------------------

# 5.1 Two cities, one year -----------------------------------------------------

# Not hand-picked: of the five cities we follow, the coldest and the hottest.
city_2019 <- hot %>% filter(year == 2019, code_muni %in% CITIES) %>% arrange(mean_temp)
city_2019

two_cities <- daily %>%
  filter(year == 2019, code_muni %in% c(first(city_2019$code_muni),
                                        last(city_2019$code_muni))) %>%
  mutate(city = fct_reorder(glue("{name_muni} ({abbrev_state})"), value))

fig10 <- ggplot(two_cities, aes(value, fill = city, colour = city)) +
  geom_density(alpha = 0.35, linewidth = 0.7) +
  geom_vline(xintercept = 30, linetype = "dashed",
             colour = INK, linewidth = 0.6) +
  annotate("text", x = 30.3, y = Inf, label = "30 C",
           hjust = 0, vjust = 1.6, size = 3.2, colour = INK) +
  scale_fill_manual(values = PAL) +
  scale_colour_manual(values = PAL) +
  labs(title    = "Daily maximum temperature, 2019",
       subtitle = "The dashed line is the bin. `hot_days` is the area to its right.",
       x = "Daily Tmax (C)", y = "Density", fill = NULL, colour = NULL) +
  theme_minimal() +
  theme(legend.position = "top")

fig10
ggsave("figures/fig10_two_cities.png", fig10,
       width = 5.2, height = 3.7, dpi = 300, bg = "white")

# The table on the frame.
two_cities %>%
  group_by(name_muni, abbrev_state) %>%
  summarise(mean_temp = mean(value), sd = sd(value), hot_30 = sum(value >= 30),
            .groups = "drop")

# 5.2 One city, two years ------------------------------------------------------

CITY_ONE <- 3550308        # a knob -- put your own city in it and rerun

two_years <- daily %>%
  filter(code_muni == CITY_ONE) %>%
  mutate(year = factor(year))

fig11 <- ggplot(two_years, aes(value, fill = year, colour = year)) +
  geom_density(alpha = 0.35, linewidth = 0.7) +
  geom_vline(xintercept = 30, linetype = "dashed",
             colour = INK, linewidth = 0.6) +
  scale_fill_manual(values = PAL) +
  scale_colour_manual(values = PAL) +
  labs(title    = glue("{first(two_years$name_muni)} ({first(two_years$abbrev_state)}): daily Tmax in 1961 and 2019"),
       subtitle = "Two years, one place. Look at the mean, then look at the tail.",
       x = "Daily Tmax (C)", y = "Density", fill = NULL, colour = NULL) +
  theme_minimal() +
  theme(legend.position = "top")

fig11
ggsave("figures/fig11_two_years.png", fig11,
       width = 5.2, height = 3.7, dpi = 300, bg = "white")

# The table on the frame.
two_years %>%
  group_by(year) %>%
  summarise(mean_temp = mean(value), sd = sd(value),
            p90 = quantile(value, 0.9), hot_30 = sum(value >= 30))
