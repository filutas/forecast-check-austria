# Project Plan: Forecast Check Austria

Owner: István Attila Filutás | Started: 2026-10-27 | Release v1.0: (fill in date) | Planned effort: about 3 working days of focused work

## 1. Goal

Measure how accurate free numerical weather forecasts are for Austrian stations, and how the error grows with forecast lead time (1 to 5 days), using only open data and a fully reproducible pipeline.

## 2. Scope

- **Stations (7, final):** Wien Hohe Warte, Graz Universität, Linz Stadt, Salzburg Flughafen, Innsbruck Flughafen, Klagenfurt Flughafen and Sonnblick (high mountain station). The list with ids and coordinates is in `config/config.yml`.
- **Variables:** 2 m air temperature (hourly) and precipitation (hourly, evaluated as daily sums). Sonnblick is evaluated for temperature only.
- **Period:** 2025-01-01 to 2025-12-31.
- **Models (3, final):** `ecmwf_ifs025`, `gfs_seamless`, `icon_seamless` from the Open-Meteo Previous Runs API.
- **Lead times:** 1, 2, 3, 4 and 5 days.
- **Metrics:** bias, MAE and RMSE for temperature; probability of detection (POD) and false alarm ratio (FAR) for rain days of 1 mm or more.
- **Deliverables:** public GitHub repository, three figures, metric tables (CSV), tests, automatic checks (CI), README with findings, release v1.0.

## 3. Out of scope

- No machine learning, bias correction or post-processing of forecasts.
- No wind, pressure, humidity or snow.
- No real-time or daily automated updates.
- No web app or dashboard (only if everything else is finished).
- No claim that results apply outside the tested stations and year.

## 4. Milestones

| ID | Milestone | Target | Status |
|----|-----------|--------|--------|
| M1 | Data access: observations and forecasts download, cached, sanity check plot is plausible | [x] |
| M2 | Merged dataset built (`data/processed/merged.parquet`), row counts checked | [x] |
| M3 | Metrics implemented with passing tests | [x] (confirm `pytest -q` passes) |
| M4 | Three figures produced and interpreted | [x] |
| M5 | README, CHANGELOG, CI green, release v1.0 published | [ ] README written; CI, changelog and release pending |

## 5. Risks

| # | Risk | Likelihood | Impact | Mitigation | Occurred? / What I did |
|---|------|-----------|--------|-----------|------------------------|
| R1 | API names, endpoints or parameters differ from what I expect | Medium | High | Verify in the documentation first, test with a tiny request, record changes in CHANGELOG | Occurred: the GeoSphere Data Hub address in my first code was outdated (host is now dataset.api.hub.geosphere.at). Found by comparing with the documentation, fixed and recorded in the CHANGELOG. |
| R2 | Rate limits or temporary API errors during download | Medium | Medium | Cache every chunk on disk, retries with back-off, pauses between requests, download in chunks | Occurred: several "connection reset" errors during the build; retries with back-off recovered automatically, no data lost. |
| R3 | Time zone or time-stamp convention mismatch between observations and forecasts | High | High | Use UTC everywhere, read the documentation of both services, sanity check plot before analysis | Checked with shift tests. Temperature: July minimum at 0 h, no problem found (January test too flat to be conclusive). Precipitation: hourly test inconclusive, mitigated by evaluating daily sums. No correction applied. |
| R4 | Missing observations or forecasts | High | Medium | Never fill gaps, drop missing rows, report counts per station, require 24 hours for daily sums | Occurred: gaps up to 120 hours at Linz; dropped, not filled. Forecasts had no gaps. |
| R5 | A model has no archived forecasts for the full period | Medium | Medium | Shorten the period or drop the model, document it | Did not occur: all three models returned complete forecasts for 2025. |
| R6 | Misleading conclusions (point station versus model grid cell, mountain station elevation) | Medium | High | State limitations in README, report station and model elevation, avoid over-claiming | Mitigated: cautious wording ("lowest error at these stations", not "best model"), limitations listed in README, Sonnblick bias reported without an unsupported explanation. |
| R7 | Environment or tooling problems (conda, Git, Windows setup) | Medium | Medium | Keep fallback (pip and venv), write problems and fixes in this plan | Occurred: conda not found in PowerShell, environment creation failed because of a conda launcher file, notebook kernel crashed when plotting. Fixed by repairing the conda installation, and plots are produced by scripts instead of notebooks. |
| R8 | Not enough time | Medium | Medium | Fixed scope, stop at the definition of done, optional extras only after M5 | Not occurred so far; the project took longer than the planned 3 days because of setup problems, scope was kept fixed. |
| R9 | Selected stations have no usable data for a variable | Medium | Medium | Test each candidate station for valid values before the big download | Occurred: Innsbruck Universität had no temperature values in the test month and was replaced by Innsbruck Flughafen; Sonnblick has no precipitation values and is evaluated for temperature only. |

## 6. Definition of done

- [x] One command (or one notebook) reproduces all figures from cached or downloaded data.
- [x] At least 6 stations, 2 models, 5 lead times, 2 variables evaluated.
- [ ] Metric functions covered by passing tests, and CI is green.
- [x] README shows the main figure, the key findings, data licences and limitations.
- [ ] PROJECT_PLAN.md lists risks that actually occurred and what was done about them (done once this version is committed).
- [ ] Tagged release v1.0.

## 7. Data facts

- Observation time stamps: returned with +00:00, treated as UTC.
- Observation precipitation (`rr`): hourly sum in mm ("Stundensumme" per dataset metadata). The metadata does not state whether the hour ends or starts at the time stamp.
- Forecast precipitation (Open-Meteo hourly): sum of the preceding hour per Open-Meteo documentation (to confirm on the documentation page before release).
- Quality flags (`tl_flag`, `rr_flag`) exist in the dataset but are not used in v1.0.
- Precipitation time convention checked empirically (lead 1, ECMWF IFS, Jul to Sep 2025, Wien/Graz/Salzburg): correlation is flat across shifts of -2 to +2 hours, inconclusive, no correction applied. Precipitation is evaluated as daily UTC sums.
- Temperature time alignment checked (Wien Hohe Warte, ECMWF IFS, lead 1): in July 2025 the mean absolute error is lowest at shift 0 h (1.26 °C) and rises on both sides (1.36 °C at -1 h, 1.48 °C at +1 h, 1.74 °C at -2 h, 1.92 °C at +2 h). The winter test (January) was inconclusive because of the weak daily cycle. Observations and forecasts are aligned in UTC, no correction applied.
- January 2025 errors, Wien Hohe Warte, ECMWF IFS: MAE grows from 1.73 °C (lead 1) to 2.69 °C (lead 5); bias between -0.31 and +0.08 °C.
- Station changes: Innsbruck Universität had no temperature values in July 2025 and was replaced by Innsbruck Flughafen. Sonnblick has no precipitation values, so it is evaluated for temperature only.
- Full-year build (2025, 7 stations, 3 models, leads 1 to 5): 919,800 merged rows, 43,800 per station and model. Forecasts have no missing values. Missing observation hours: temperature Linz 120, Wien 32, Klagenfurt 24, Salzburg 6, others 0; precipitation Graz 1, Klagenfurt 2, Sonnblick 8,758 (no precipitation measurement).
- Missing values are dropped in the metrics and never filled. Daily precipitation sums use only days with all 24 hours present.
- Models changed because of availability: none. All three models returned complete forecasts for Q1 2025 and for the full year.

## 8. Results notes

- Error grows with lead time for every model: temperature MAE 1.16 to 1.98 °C at day 1 and 2.15 to 2.42 °C at day 5 (mean over 7 stations).
- ICON seamless has the lowest short-range error (1.16 °C at day 1 against 1.72 °C ECMWF and 1.98 °C GFS), but by day 5 it is equal to ECMWF (2.15 and 2.17 °C).
- Mean temperature bias at lead 1 is small (ECMWF -0.50 °C, GFS +0.03 °C, ICON +0.14 °C), except at Sonnblick (ECMWF -1.70 °C, GFS -1.09 °C, ICON +0.25 °C). Cause not investigated.
- Rain days (at least 1 mm, 6 stations): POD falls from 0.84 to 0.89 (day 1) to 0.54 to 0.74 (day 5); FAR rises from 0.22 to 0.34 (day 1) to 0.42 to 0.47 (day 5). ECMWF has the highest POD at every lead time.
- Statements apply to these stations, this year and these model products only.

## 9. Open items before release

- [ ] Run `pytest -q` and `ruff check src tests`; fix any messages.
- [ ] Add `.github/workflows/ci.yml` and confirm a green check in the Actions tab.
- [ ] Create CHANGELOG.md.
- [ ] Confirm the Open-Meteo precipitation convention in their documentation.
- [ ] Optional: run `src/check_elevation.py` for the Sonnblick paragraph.
- [ ] Fresh-start test of the README quick start in a new folder.
- [ ] Publish release v1.0, add repository description and topics, pin the repository.
- [ ] Close the M1 to M5 issues on the GitHub board.