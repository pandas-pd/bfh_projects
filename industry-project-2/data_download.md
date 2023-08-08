# Set-up: Copernicus api download (Windows OS)
- Install the cds api library into the python environment by running the command:

```python
#if pip was added to path
pip install cdsapi

#if pip was not added to path
py -m pip install cdsapi
```

- Retrieve your API Key from the CDS Website:
    - Open: https://cds.climate.copernicus.eu/#!/home
    - Login with your credentials
    - Go to User and scroll to the bottom. The ```url``` and ```key``` should be listed there.
- Create a new file in your home directory (if you are using Windows, this will be something like C:\Users\UserName)
    - filename: ```.cdsapirc```
    - contents (pasted from the Copernicus Website):

```
url: your_url
key: your_key
```

- Open the ```main_0.ipynb``` file:
    - Go to cell 4
    - Set the parameters accordingly
    - If all data should be downloaded and recompiled, set all parameters to true. Note that if the ```save_data``` paramtere is set to true, all your data in the according data_folder will be overwritten
    - Total data size: 163 GB, total approximat download time: 4 - 7 days (cannot be accelerated by multi-threading or -processing, due to the queueing system of the api)

```python
#general parsing and aggregating of files
save_data                   = True

#chapter 0.1
t2_run_era5_download        = True
t2m_compile_df              = True

#chapter 0.2
soi_run_era5_download       = True
soi_compile_df              = True

#chapter 0.5
pv_run_era5_download        = True
pv_compile_df               = True
```

- Additional Links:
    - Official setup guide: https://cds.climate.copernicus.eu/api-how-to#install-the-cds-api-key
    - Alternative installation with colab (not tested): https://stackoverflow.com/questions/64304862/using-cdsapi-in-google-colab