# BTHE - Bachelor thesis

## Roadmap / Meetings
- 2023-02-27 16:30, Kick-off meeting
- 2023-02-28 23:59, hand-in Project disposition
- 2023-04-01, 23:59, hand-in industry project 2

## Links and data sources
- Weather data at: https://cds.climate.copernicus.eu/#!/home
- Tutorial video: https://www.youtube.com/watch?v=AXG97K6NYD8
- ENSO: https://www.climate.gov/news-features/blogs/enso/what-el-ni%C3%B1o%E2%80%93southern-oscillation-enso-nutshell

## ToDo
1. Get to know data source by registering at and exploring https://cds.climate.copernicus.eu/
Introduction video, e.g., https://www.youtube.com/watch?v=AXG97K6NYD8
2. To forecast the heating demand, the single most important variable is the outside air temperature.
- Download ERA5 reanalyis, variable name = „2m temperature“
- Compile “climatology” benchmark: monthly mean and std of 2m air temperature of last 30 years in Switzerland
- Forecast anomalies in monthly mean 2m air temperatures (Y) using El Nino Southern Oscillation (ENSO) index (X1)
    - Download ENSO index (or compute it yourself ;-))
    - Add Madden Julian Oscillation (MJO) index as a second feature (X2) in ML model
    - Train and test an ML model, using the features X1 and possibly X2 to forecast Y of next months 
- Compare the forecast skill of the model (RMSE in 2m temp anomalies) with the “climatology” benchmark
3. Compare the forecast skill of the model with the forecast skill of operational subseasonal forecast products from operational centers like UKMO, NCEP, CMA— similar to https://journals.ametsoc.org/view/journals/wefo/36/1/waf-d-20-0096.1.xml (but for Switzerland)

## Datasets and Sources
- Copernicus climat data:
    - Variouse:
        - https://cds.climate.copernicus.eu/cdsapp#!/dataset/ecv-for-climate-change?tab=overview
        - https://cds.climate.copernicus.eu/cdsapp#!/dataset/derived-reanalysis-energy-moisture-budget?tab=overview
    - Hourly (temp, pres):
        - https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview
        - https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=overview
    - Monthly (temp, pres):
        - https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land-monthly-means?tab=overview
        - https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land?tab=overview
- Enso Index data:
    - https://psl.noaa.gov/enso/mei/
    - https://psl.noaa.gov/enso/data.html
    - https://climatedataguide.ucar.edu/climate-data/multivariate-enso-index
- MJO Index data:
    - https://iridl.ldeo.columbia.edu/SOURCES/.BoM/.MJO/.RMM/datasetdatafiles.html
    - http://www.bom.gov.au/climate/mjo/
- Heating demand data Switzerland:
    - Papers:
        - file:///C:/Users/joelt/Downloads/9777-Modelldokumentation_MGDM_Thermische_Netze_DE_PDF_V1rev2.pdf
        - https://sccer-jasm.ch/JASMpapers/JASM_time_series.pdf
    - Data Sources geoCat (https://www.geocat.ch/geonetwork/srv/ger/catalog.search#/home):
        - https://www.geocat.ch/geonetwork/srv/ger/catalog.search#/metadata/32a8a3cd-d269-4915-b983-54fd979ca486
        - https://www.geocat.ch/geonetwork/srv/ger/catalog.search#/metadata/25de2a79-1714-4db8-a7ad-48efc8a4f5c7
        - https://www.geocat.ch/geonetwork/srv/ger/catalog.search#/metadata/44598622-14ca-4937-a65b-3d3c2207f8a5
    - Data Sources JASM:
        - https://data.sccer-jasm.ch/demand-hourly-profile-retrofits-cesar/
        - https://data.sccer-jasm.ch/demand-hourly-profile-hsr/2020-12-10/
        - https://data.sccer-jasm.ch/demand-hourly-profile/2019-02-27/
        - https://data.sccer-jasm.ch/building-stock/2020-04-20/
- Polar vortex data
    - Pressure calculator (10 hPa = 25'000 m altitude (approx.))
        - https://www.mide.com/air-pressure-at-altitude-calculator
        - https://www.madur.com/index.php?page=/altitude
    - Era5 wind component data (v, U, Vertical wind speeds, Lon lat limits tbd):
        - https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=form

