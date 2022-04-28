# Energy ETL

This pipeline takes three datasets:</br>

- temperature data</br>

- energy production and consumption</br>

- greenhouse gas emissions</br>

transforms them into dimensional model in Amazon Redshift.</br></br>

## Usage

- You will need a Redshift cluster and S3 bucket.</br> 
    > Your S3 bucket will be used to upload clean datasets and then load them into staging in Redshift. 
- Next use config template `gbs_energy_etl/aws_template.cfg` to add your AWS IAM, Redshift and S3 details. Do not change the order of fields.

- Either add path of your config file to CFG_PATH environment variable or save it as `/gbs_energy_etl/aws.cfg`.

- Install dependencies from requirements.txt

- Run `main_connector.py`</br></br>

## About source datasets

### "GlobalLandTemperaturesByCountry"

This temperature data comes from Berkeley Earth which is an independent U.S. non-profit organisation focused on environmental data science. Data range covered is between 1743-2013.</br>

![temperature dataset sample](/img/temp.png)</br>

<font  size=2>source: https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data</font></br>
<font  size=2>licence: https://creativecommons.org/licenses/by-nc-sa/4.0/</font></br></br>

### "CW_HistoricalEmissions"

Climate Watch is an online platform designed to provide open climate data. It is managed by World Resources Institute. Data contains historical greenhouse gas emissions per country, per year, per gas and covers years from 1850 to 2018.</br>

![emissions dataset sample](/img/emissions.png)</br>

<font  size=2>source: https://www.climatewatchdata.org/data-explorer/historical-emissions</font></br>
<font  size=2>licence: https://www.climatewatchdata.org/about/permissions</font></br>
<font  size=2>more info: https://zenodo.org/record/4479172#.Yg0yei-l06V</font></br></br>

### "OWID-energy-data"

Our World In Data is a non-profit organization providing data to tackle variety of issues. Dataset contains information about amounts of energy consumption and production by type, by country, by year. Data range covered is between 1900-2021.</br>

![energy dataset sample](/img/energy.png)</br>

<font  size=2>source: https://github.com/owid/energy-data</font></br>
<font  size=2>licence: https://creativecommons.org/licenses/by/4.0/</font></br></br>

## About final model

Final tables show historical temperature, gas emissions as well as energy production and consumption,
by year, by country. Data covers time range from 1900 to 2021.</br></br>

