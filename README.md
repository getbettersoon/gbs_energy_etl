# Energy ETL

This pipeline takes three datasets from my bucket in Amazon S3:
- temperature data
- energy production and consumption
- greenhouse gas emissions

and transforms them into dimensional model in Amazon Redshift. 


# Usage

## set up environment

- You will need a Redshift cluster. Next add cluster/AWS details to aws_template.cfg.  
Do not change the order of fields.

- Add path of your config file to CFG_PATH environment variable  
or save it as `/gbs_energy_etl/aws.cfg`.

## run the script

- Run `gbs_energy_etl/create_tables.py`
- Run `gbs_energy_etl/etl.py`
> podac cala sciezke z root czy tylko nazwe pliku?


## about source datasets

### "GlobalLandTemperaturesByCountry"
		
This temperature data comes from Berkeley Earth which is an independent U.S. non-profit organisation focused on environmental data science. Data range covered is between 1743-2013.
![temperature dataset sample](/img/temp.png)
source: (https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data)
licence: (https://creativecommons.org/licenses/by-nc-sa/4.0/)

### "CW_HistoricalEmissions"

Climate Watch is an online platform designed to provide open climate data. It is managed by World Resources Institute. 
Data contains historical greenhouse gas emissions per country, per year, per gas. Data covers years from 1850-2018.
![emissions dataset sample](/img/emissions.png)
source: (https://www.climatewatchdata.org/data-explorer/historical-emissions)
licence: (https://www.climatewatchdata.org/about/permissions)
more info: (https://zenodo.org/record/4479172#.Yg0yei-l06V)

### "OWID-energy-data"

Our World In Data is a non-profit organization providing data to tackle variety of issues.
Dataset contains information about amounts of energy consumption and production by type, by country, by year. Data range covered is between 1900-2021.
![energy dataset sample](/img/energy.png)
source: (https://github.com/owid/energy-data)
licence: (https://creativecommons.org/licenses/by/4.0/)


## about final model
Final tables show historical temperature, gas emissions as well as energy production and consumption, 
by year, by country. Data covers time range from 1900 to 2021.