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
| M1 | Data access: observations and forecasts download, cached, sanity check plot is plausible | Day 1 | [ ] |
| M2 | Merged dataset built (`data/processed/merged.parquet`), row counts checked | Day 2 | [ ] |
| M3 | Metrics implemented with passing tests | Day 2 | [ ] |
| M4 | Three figures produced and interpreted | Day 3 | [ ] |
| M5 | README, CHANGELOG, CI green, release v1.0 published | Day 3 | [ ] |

## 5. Risks

| # | Risk | Likelihood | Impact | Mitigation | Occurred? / What I did |
|---|------|-----------|--------|-----------|------------------------|
| R1 | API names, endpoints or parameters differ from what I expect | Medium | High | Verify in the documentation first, test with a tiny request, record changes in CHANGELOG | |
| R2 | Rate limits or temporary API errors during download | Medium | Medium | Cache every chunk on disk, retries with back-off, pauses between requests, download in chunks | |
| R3 | Time zone or time-stamp convention mismatch between observations and forecasts | High | High | Use UTC everywhere, read the documentation of both services, sanity check plot before analysis | |
| R4 | Missing observations or forecasts | High | Medium | Never fill gaps, drop missing rows, report counts per station, require 24 hours for daily sums | |
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

(Fill in during Parts 6 and 8.)

- Observation time stamps are in: (UTC? check documentation)
- Hourly precipitation in the observations is the sum over: (hour ending at the time stamp? check documentation)
- Forecast precipitation (Open-Meteo hourly) is the sum over: (preceding hour per documentation, confirm)
- Rows with missing values per station: 
- How missing values were handled: dropped, never filled
- Models or periods changed because of availability: