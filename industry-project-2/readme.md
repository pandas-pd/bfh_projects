# Bachelor thesis pre project
Contents of the pre-project to my bachelor thesis. See paper for additionalo information.

## Enviroment, needed pakcages
- sklearn
- pandas
- numpy
- plotly.express
- tensorflow / keras
## data sources:
- t2m:
    - https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview
- soi:
    - https://www.longpaddock.qld.gov.au/soi/soi-data-files/
    - https://iridl.ldeo.columbia.edu/maproom/ENSO/Time_Series/Equatorial_SOI.html
    - https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview
- mjo:
    - http://www.bom.gov.au/climate/mjo/
- nao:
    - https://psl.noaa.gov/data/timeseries/daily/NAO/
    - https://downloads.psl.noaa.gov/Public/map/teleconnections/nao.reanalysis.t10trunc.1948-present.txt
- Custom polar vortex data
    - https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=form
- ao:
    - https://ftp.cpc.ncep.noaa.gov/cwlinks/
    - https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/ao.shtml
## tutorials and resources:
- multistep ahead forecasting with sklearn:
    - https://forecastegy.com/posts/multiple-time-series-forecasting-with-scikit-learn/#recursive-vs-direct-forecasting
## steps for the thesis:
- gather all data:
    - calculate the soi
    - define a custome polar vortex index (identify beark downs or some sort of break down index)
- explore data
- feaute engineering and predition type fixing (two dataframes for classificaiton and regression)
- modeling
