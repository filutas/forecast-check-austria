# forecast-check-austria
Verification of free weather forecasts against Austrian station measurements

# limitations
The time convention of hourly precipitation could not be confirmed empirically; precipitation is evaluated as daily sums to limit the effect of a possible one-hour offset.


# details
- gfs_seamless and icon_seamless are Open-Meteo’s blended products, which may combine several model versions or resolutions for one location. Write the model names exactly as used, and don’t call them plain “GFS” or “ICON” in your findings.
- The model grids differ in resolution (ECMWF IFS at 0.25° is coarse, about 25 km). Mention this in the limitations when you explain station bias, especially at Sonnblick and Innsbruck.