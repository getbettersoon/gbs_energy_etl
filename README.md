# energy ETL

This pipeline takes three datasets:
- temperature data
- energy production and consumption
- greenhouse gas emissions

and combines them into dimensional model.


# usage

## set up environment

- You will need a Redshift cluster. Next add cluster/AWS details to aws_template.cfg.  
Do not change the order of fields.

- Add path to your config file to CFG_PATH environment variable  
or save it as `/gbs_energy_etl/aws.cfg`.

## run the script

- Run `gbs_energy_etl/create_tables.py`
- Run `gbs_energy_etl/etl.py`
> podac cala sciezke z root czy tylko nazwe pliku?


