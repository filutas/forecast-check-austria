# Project Plan: Forecast Check Austria

Owner: István Attila Filutás | Started: 2026-10-27 | Target release: v1.0 within 3 working days

## 1. Goal
Measure how accurate free numerical weather forecasts are for Austrian stations, and how the error grows with forecast lead time (1 to 5 days), using only open data and a fully reproducible pipeline.

## 2. Scope
- **Stations:** 6 to 8 GeoSphere Austria stations in different terrain (Vienna, Graz, Linz, Salzburg, Innsbruck, Klagenfurt, and one high mountain station such as Sonnblick). Final list is in `config/config.yml`.
- **Variables:** 2 m air temperature (hourly) and precipitation (hourly, evaluated as daily sums).
- **Period:** 2025-01-01 to 2025-12-31 (shortened if a model has no archived forecasts for the full period).
- **Models:** 2 to 3 from the Open-Meteo Previous Runs API (planned: `ecmwf_ifs025`, `gfs_seamless`, `icon_seamless`; subject to availability).
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
| M1 | Data access: observations and forecasts download, cached, sanity check plot is plausible | Day 1 | [X] |
| M2 | Merged dataset built (`data/processed/merged.parquet`), row counts checked | Day 2 | [ ] |
| M3 | Metrics implemented with passing tests | Day 2 | [ ] |
| M4 | Three figures produced and interpreted | Day 3 | [ ] |
| M5 | README, CHANGELOG, CI green, release v1.0 published | Day 3 | [ ] |

## 5. Risks

| # | Risk | Likelihood | Impact | Mitigation | Occurred? / What I did |
|---|------|-----------|--------|-----------|------------------------|
| R1 | API names, endpoints or parameters differ from what I expect | Medium | High | Verify in the documentation first, test with a tiny request, record changes in CHANGELOG | |
| R2 | Rate limits or temporary API errors during download | Medium | Medium | Cache every chunk on disk, retries with back-off, pauses between requests, download in chunks |Occurred: several “connection reset” errors during the build; retries with back-off recovered automatically, no data lost. |
| R3 | Time zone or time-stamp convention mismatch between observations and forecasts | High | High | Use UTC everywhere, read the documentation of both services, sanity check plot before analysis | Checked with a shift test, inconclusive, mitigated by daily sums. Checked with a shift test in July, minimum at 0 h, no problem found.|
| R4 | Missing observations or forecasts | High | Medium | Never fill gaps, drop missing rows, report counts per station, require 24 hours for daily sums | Occurred: gaps up to 120 hours at Linz; dropped, not filled |
| R5 | A model has no archived forecasts for the full period | Medium | Medium | Shorten the period or drop the model, document it | |
| R6 | Misleading conclusions (point station versus model grid cell, mountain station elevation) | Medium | High | State limitations in README, report station and model elevation, avoid over-claiming | |
| R7 | Environment or tooling problems (conda, Git, Windows setup) | Medium | Medium | Keep fallback (pip and venv), write problems and fixes in this plan | |
| R8 | Not enough time | Medium | Medium | Fixed scope, stop at the definition of done, optional extras only after M5 | |

## 6. Definition of done

- One command (or one notebook) reproduces all figures from cached or downloaded data.
- At least 6 stations, 2 models, 5 lead times, 2 variables evaluated.
- Metric functions covered by passing tests, and CI is green.
- README shows the main figure, the three key findings, data licences and limitations.
- PROJECT_PLAN.md lists risks that actually occurred and what was done about them.
- Tagged release v1.0.

## 7. Data facts

- Observation time stamps: returned with +00:00, treated as UTC.
- Observation precipitation (`rr`): hourly sum in mm ("Stundensumme" per dataset metadata). The metadata does not state whether the hour ends or starts at the time stamp.
- Forecast precipitation (Open-Meteo hourly): sum of the preceding hour per Open-Meteo documentation (to confirm).
- Quality flags (`tl_flag`, `rr_flag`) exist in the dataset but are not used in v1.0.
- Precipitation time convention checked empirically (lead 1, ECMWF IFS, Jul to Sep 2025, Wien/Graz/Salzburg): correlation is flat across shifts of -2 to +2 hours, inconclusive, no correction applied. Precipitation is evaluated as daily UTC sums.
- Temperature time alignment checked (Wien Hohe Warte, ECMWF IFS, lead 1): in July 2025 the mean absolute error is lowest at shift 0 h (1.26 °C) and rises on both sides (1.36 °C at -1 h, 1.48 °C at +1 h, 1.74 °C at -2 h, 1.92 °C at +2 h). The winter test (January) was inconclusive because of the weak daily cycle. Observations and forecasts are aligned in UTC, no correction applied.
- January 2025 errors, Wien Hohe Warte, ECMWF IFS: MAE grows from 1.73 °C (lead 1) to 2.69 °C (lead 5); bias between -0.31 and +0.08 °C.
- Station changes: Innsbruck Universität had no temperature values in July 2025 and was replaced by Innsbruck Flughafen. Sonnblick has no precipitation values, so it is evaluated for temperature only.
- Full-year build (2025, 7 stations, 3 models, leads 1 to 5): 919,800 merged rows, 43,800 per station and model. Forecasts have no missing values. Missing observation hours: temperature Linz 120, Wien 32, Klagenfurt 24, Salzburg 6, others 0; precipitation Graz 1, Klagenfurt 2, Sonnblick 8,758 (no precipitation measurement).
- Missing values are dropped in the metrics and never filled. Daily precipitation sums use only days with all 24 hours present.
- Models changed because of availability: none.
- Models checked for Q1 2025 (Wien Hohe Warte, leads 1 to 5): ecmwf_ifs025, gfs_seamless and icon_seamless all return 10800 rows with no missing values. No model removed so far. Full-year completeness is checked in the build_dataset printout.
