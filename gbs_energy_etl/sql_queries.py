from settings import config


ROLE_ARN = config.get('IAM_ROLE', 'ROLE_ARN')


# DROP TABLES
staging_temp_table_drop = "DROP TABLE IF EXISTS staging_temp"
staging_emissions_table_drop = "DROP TABLE IF EXISTS staging_emissions"
staging_energy_table_drop = "DROP TABLE IF EXISTS staging_energy"
date_table_drop = "DROP TABLE IF EXISTS date CASCADE"
country_table_drop = "DROP TABLE IF EXISTS country CASCADE"
fact_table_drop = "DROP TABLE IF EXISTS fact CASCADE"


# CREATE TABLES
staging_temp_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_temp (
    dt DATE NOT NULL,
    average_temp DECIMAL(5,2),
    country TEXT NOT NULL
)
""")

staging_emissions_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_emissions (
    iso_code CHAR(3) NOT NULL,
    gas VARCHAR(10) NOT NULL,
    year INT2 NOT NULL,
    emission_amount FLOAT NOT NULL
)
""")

staging_energy_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_energy (
    country TEXT NOT NULL,
    iso_code CHAR(3) NOT NULL,
    year INT2 NOT NULL,
    population INT,
    gdp BIGINT,
    energy_metric VARCHAR(50) NOT NULL,
    energy_amount FLOAT
)
""")


date_table_create = ("""
CREATE TABLE IF NOT EXISTS date (
    date_id INT IDENTITY(0,1),
    year INT2 NOT NULL,
    PRIMARY KEY(date_id))
SORTKEY(year)
""")


country_table_create = ("""
CREATE TABLE IF NOT EXISTS country (
    country_id INT IDENTITY(0,1),
    name TEXT,
    iso_code CHAR(3),
    PRIMARY KEY (country_id))
SORTKEY(name)
""")

fact_table_create = ("""
CREATE TABLE IF NOT EXISTS fact (
    date_id INT,
    country_id INT,
    temperature FLOAT,
    co2_emissions FLOAT,
    ch4_emissions FLOAT,
    n2o_emissions FLOAT,
    population INT,
    gdp BIGINT,
    coal_production FLOAT,
    coal_prod_change_pct FLOAT,
    coal_prod_change_twh FLOAT,
    coal_prod_per_capita FLOAT,
    coal_consumption FLOAT,
    coal_cons_change_pct FLOAT,
    coal_cons_change_twh FLOAT,
    coal_cons_per_capita FLOAT,
    coal_electricity FLOAT,
    coal_elec_per_capita FLOAT,
    coal_share_elec FLOAT,
    coal_share_energy FLOAT,
    oil_production FLOAT,
    oil_prod_change_pct FLOAT,
    oil_prod_change_twh FLOAT,
    oil_prod_per_capita FLOAT,
    oil_consumption FLOAT,
    oil_cons_change_pct FLOAT,
    oil_cons_change_twh FLOAT,
    oil_electricity FLOAT,
    oil_elec_per_capita FLOAT,
    oil_energy_per_capita FLOAT,
    oil_share_elec FLOAT,
    oil_share_energy FLOAT,
    gas_production FLOAT,
    gas_prod_change_pct FLOAT,
    gas_prod_change_twh FLOAT,
    gas_prod_per_capita FLOAT,
    gas_consumption FLOAT,
    gas_cons_change_pct FLOAT,
    gas_cons_change_twh FLOAT,
    gas_electricity FLOAT,
    gas_elec_per_capita FLOAT,
    gas_energy_per_capita FLOAT,
    gas_share_elec FLOAT,
    gas_share_energy FLOAT,
    fossil_fuel_consumption FLOAT,
    fossil_cons_change_pct FLOAT,
    fossil_cons_change_twh FLOAT,
    fossil_cons_per_capita FLOAT,
    fossil_electricity FLOAT,
    fossil_energy_per_capita FLOAT,
    fossil_share_elec FLOAT,
    fossil_share_energy FLOAT,
    biofuel_consumption FLOAT,
    biofuel_cons_change_pct FLOAT,
    biofuel_cons_change_twh FLOAT,
    biofuel_cons_per_capita FLOAT,
    biofuel_electricity FLOAT,
    biofuel_elec_per_capita FLOAT,
    biofuel_share_elec FLOAT,
    biofuel_share_energy FLOAT,
    low_carbon_consumption FLOAT,
    low_carbon_cons_change_pct FLOAT,
    low_carbon_cons_change_twh FLOAT,
    low_carbon_electricity FLOAT,
    low_carbon_elec_per_capita FLOAT,
    low_carbon_share_elec FLOAT,
    low_carbon_share_energy FLOAT,
    nuclear_consumption FLOAT,
    nuclear_cons_change_pct FLOAT,
    nuclear_cons_change_twh FLOAT,
    nuclear_electricity FLOAT,
    nuclear_elec_per_capita FLOAT,
    nuclear_energy_per_capita FLOAT,
    nuclear_share_elec FLOAT,
    nuclear_share_energy FLOAT,
    wind_consumption FLOAT,
    wind_cons_change_pct FLOAT,
    wind_cons_change_twh FLOAT,
    wind_electricity FLOAT,
    wind_elec_per_capita FLOAT,
    wind_energy_per_capita FLOAT,
    wind_share_elec FLOAT,
    wind_share_energy FLOAT,
    solar_consumption FLOAT,
    solar_cons_change_pct FLOAT,
    solar_cons_change_twh FLOAT,
    solar_electricity FLOAT,
    solar_elec_per_capita FLOAT,
    solar_energy_per_capita FLOAT,
    solar_share_elec FLOAT,
    solar_share_energy FLOAT,
    hydro_consumption FLOAT,
    hydro_cons_change_pct FLOAT,
    hydro_cons_change_twh FLOAT,
    hydro_electricity FLOAT,
    hydro_elec_per_capita FLOAT,
    hydro_energy_per_capita FLOAT,
    hydro_share_elec FLOAT,
    hydro_share_energy FLOAT,
    renewables_consumption FLOAT,
    renewables_cons_change_pct FLOAT,
    renewables_electricity FLOAT,
    renewables_elec_per_capita FLOAT,
    renewables_energy_per_capita FLOAT,
    renewables_share_energy FLOAT,
    renewables_share_elec FLOAT,
    other_renewables_consumption FLOAT,
    other_renewables_cons_change_pct FLOAT,
    other_renewables_cons_change_twh FLOAT,
    other_renewables_electricity FLOAT,
    other_renewables_elec_per_capita FLOAT,
    other_renewables_energy_per_capita FLOAT,
    other_renewables_share_elec FLOAT,
    other_renewables_share_energy FLOAT,
    other_renewables_electricity_exc_biofuel FLOAT,
    other_renewables_elec_per_capita_exc_biofuel FLOAT,
    other_renewables_share_elec_exc_biofuel FLOAT,
    primary_energy_consumption FLOAT,
    energy_cons_change_pct FLOAT,
    energy_cons_change_twh FLOAT,
    per_capita_electricity FLOAT,
    energy_per_capita FLOAT,
    energy_per_gdp FLOAT,
    PRIMARY KEY (date_id, country_id),
    FOREIGN KEY (date_id) REFERENCES date(date_id),
    FOREIGN KEY (country_id) REFERENCES country(country_id)
)
SORTKEY (country_id, date_id)
""")


# STAGING TABLES COPY
staging_temp_copy = ("""
    COPY staging_temp
    FROM 's3://gbs-energy/clean_GlobalLandTemperaturesByCountry.csv'
    iam_role '{}'
    CSV
    IGNOREHEADER 1
    DELIMITER ','
    region 'us-west-2'
    """.format(ROLE_ARN)
)

staging_emissions_copy = ("""
    COPY staging_emissions
    FROM 's3://gbs-energy/clean_CW_HistoricalEmissions_PIK.csv'
    iam_role '{}'
    CSV
    IGNOREHEADER 1
    DELIMITER ','
    region 'us-west-2'
""".format(ROLE_ARN)
)

staging_energy_copy = ("""
    COPY staging_energy
    FROM 's3://gbs-energy/clean_owid-energy-data.json'
    iam_role '{}'
    json 'auto'
    compupdate off
    region 'us-west-2'
""".format(ROLE_ARN)
)


# INSERT TABLES

country_table_insert = ("""
INSERT INTO country (name, iso_code)
SELECT DISTINCT country, iso_code
FROM staging_energy
""")

date_table_insert = ("""
INSERT INTO date (year)
(SELECT year FROM staging_emissions
UNION
SELECT year FROM staging_energy)
""")

fact_table_insert = ("""
INSERT INTO fact (date_id, country_id, temperature, co2_emissions,
    ch4_emissions, n2o_emissions, population, gdp, coal_production,
    coal_prod_change_pct, coal_prod_change_twh, coal_prod_per_capita,
    coal_consumption, coal_cons_change_pct, coal_cons_change_twh,
    coal_cons_per_capita, coal_electricity, coal_elec_per_capita,
    coal_share_elec, coal_share_energy, oil_production,
    oil_prod_change_pct, oil_prod_change_twh, oil_prod_per_capita,
    oil_consumption, oil_cons_change_pct, oil_cons_change_twh,
    oil_electricity, oil_elec_per_capita, oil_energy_per_capita,
    oil_share_elec, oil_share_energy, gas_production,
    gas_prod_change_pct, gas_prod_change_twh, gas_prod_per_capita,
    gas_consumption, gas_cons_change_pct, gas_cons_change_twh,
    gas_electricity, gas_elec_per_capita, gas_energy_per_capita,
    gas_share_elec, gas_share_energy, fossil_fuel_consumption,
    fossil_cons_change_pct, fossil_cons_change_twh,
    fossil_cons_per_capita, fossil_electricity,
    fossil_energy_per_capita, fossil_share_elec, fossil_share_energy,
    biofuel_consumption, biofuel_cons_change_pct,
    biofuel_cons_change_twh, biofuel_cons_per_capita,
    biofuel_electricity, biofuel_elec_per_capita, biofuel_share_elec,
    biofuel_share_energy, low_carbon_consumption,
    low_carbon_cons_change_pct, low_carbon_cons_change_twh,
    low_carbon_electricity, low_carbon_elec_per_capita,
    low_carbon_share_elec, low_carbon_share_energy,
    nuclear_consumption, nuclear_cons_change_pct,
    nuclear_cons_change_twh, nuclear_electricity,
    nuclear_elec_per_capita, nuclear_energy_per_capita,
    nuclear_share_elec, nuclear_share_energy, wind_consumption,
    wind_cons_change_pct, wind_cons_change_twh, wind_electricity,
    wind_elec_per_capita, wind_energy_per_capita, wind_share_elec,
    wind_share_energy, solar_consumption, solar_cons_change_pct,
    solar_cons_change_twh, solar_electricity, solar_elec_per_capita,
    solar_energy_per_capita, solar_share_elec, solar_share_energy,
    hydro_consumption, hydro_cons_change_pct, hydro_cons_change_twh,
    hydro_electricity, hydro_elec_per_capita, hydro_energy_per_capita,
    hydro_share_elec, hydro_share_energy, renewables_consumption,
    renewables_cons_change_pct, renewables_electricity,
    renewables_elec_per_capita, renewables_energy_per_capita,
    renewables_share_energy, renewables_share_elec,
    other_renewables_consumption, other_renewables_cons_change_pct,
    other_renewables_cons_change_twh, other_renewables_electricity,
    other_renewables_elec_per_capita,
    other_renewables_energy_per_capita, other_renewables_share_elec,
    other_renewables_share_energy,
    other_renewables_electricity_exc_biofuel,
    other_renewables_elec_per_capita_exc_biofuel,
    other_renewables_share_elec_exc_biofuel,
    primary_energy_consumption, energy_cons_change_pct,
    energy_cons_change_twh, per_capita_electricity,
    energy_per_capita, energy_per_gdp)

WITH emissions AS (
SELECT iso_code, year,
    SUM(CASE WHEN gas = 'CO2' THEN emission_amount END) AS co2_emissions,
    SUM(CASE WHEN gas = 'CH4' THEN emission_amount END) AS ch4_emissions,
    SUM(CASE WHEN gas = 'N2O' THEN emission_amount END) AS n2o_emissions
FROM
    staging_emissions
GROUP BY iso_code, year
  ),

  energy AS (
  SELECT iso_code, country, year, population, gdp,
  SUM(CASE WHEN energy_metric='coal_production' THEN energy_amount END) AS coal_production,
  SUM(CASE WHEN energy_metric='coal_prod_change_pct' THEN energy_amount END) AS coal_prod_change_pct,
  SUM(CASE WHEN energy_metric='coal_prod_change_twh' THEN energy_amount END) AS coal_prod_change_twh,
  SUM(CASE WHEN energy_metric='coal_prod_per_capita' THEN energy_amount END) AS coal_prod_per_capita,
  SUM(CASE WHEN energy_metric='coal_consumption' THEN energy_amount END) AS coal_consumption,
  SUM(CASE WHEN energy_metric='coal_cons_change_pct' THEN energy_amount END) AS coal_cons_change_pct,
  SUM(CASE WHEN energy_metric='coal_cons_change_twh' THEN energy_amount END) AS coal_cons_change_twh,
  SUM(CASE WHEN energy_metric='coal_cons_per_capita' THEN energy_amount END) AS coal_cons_per_capita,
  SUM(CASE WHEN energy_metric='coal_electricity' THEN energy_amount END) AS coal_electricity,
  SUM(CASE WHEN energy_metric='coal_elec_per_capita' THEN energy_amount END) AS coal_elec_per_capita,
  SUM(CASE WHEN energy_metric='coal_share_elec' THEN energy_amount END) AS coal_share_elec,
  SUM(CASE WHEN energy_metric='coal_share_energy' THEN energy_amount END) AS coal_share_energy,
  SUM(CASE WHEN energy_metric='oil_production' THEN energy_amount END) AS oil_production,
  SUM(CASE WHEN energy_metric='oil_prod_change_pct' THEN energy_amount END) AS oil_prod_change_pct,
  SUM(CASE WHEN energy_metric='oil_prod_change_twh' THEN energy_amount END) AS oil_prod_change_twh,
  SUM(CASE WHEN energy_metric='oil_prod_per_capita' THEN energy_amount END) AS oil_prod_per_capita,
  SUM(CASE WHEN energy_metric='oil_consumption' THEN energy_amount END) AS oil_consumption,
  SUM(CASE WHEN energy_metric='oil_cons_change_pct' THEN energy_amount END) AS oil_cons_change_pct,
  SUM(CASE WHEN energy_metric='oil_cons_change_twh' THEN energy_amount END) AS oil_cons_change_twh,
  SUM(CASE WHEN energy_metric='oil_electricity' THEN energy_amount END) AS oil_electricity,
  SUM(CASE WHEN energy_metric='oil_elec_per_capita' THEN energy_amount END) AS oil_elec_per_capita,
  SUM(CASE WHEN energy_metric='oil_energy_per_capita' THEN energy_amount END) AS oil_energy_per_capita,
  SUM(CASE WHEN energy_metric='oil_share_elec' THEN energy_amount END) AS oil_share_elec,
  SUM(CASE WHEN energy_metric='oil_share_energy' THEN energy_amount END) AS oil_share_energy,
  SUM(CASE WHEN energy_metric='gas_production' THEN energy_amount END) AS gas_production,
  SUM(CASE WHEN energy_metric='gas_prod_change_pct' THEN energy_amount END) AS gas_prod_change_pct,
  SUM(CASE WHEN energy_metric='gas_prod_change_twh' THEN energy_amount END) AS gas_prod_change_twh,
  SUM(CASE WHEN energy_metric='gas_prod_per_capita' THEN energy_amount END) AS gas_prod_per_capita,
  SUM(CASE WHEN energy_metric='gas_consumption' THEN energy_amount END) AS gas_consumption,
  SUM(CASE WHEN energy_metric='gas_cons_change_pct' THEN energy_amount END) AS gas_cons_change_pct,
  SUM(CASE WHEN energy_metric='gas_cons_change_twh' THEN energy_amount END) AS gas_cons_change_twh,
  SUM(CASE WHEN energy_metric='gas_electricity' THEN energy_amount END) AS gas_electricity,
  SUM(CASE WHEN energy_metric='gas_elec_per_capita' THEN energy_amount END) AS gas_elec_per_capita,
  SUM(CASE WHEN energy_metric='gas_energy_per_capita' THEN energy_amount END) AS gas_energy_per_capita,
  SUM(CASE WHEN energy_metric='gas_share_elec' THEN energy_amount END) AS gas_share_elec,
  SUM(CASE WHEN energy_metric='gas_share_energy' THEN energy_amount END) AS gas_share_energy,
  SUM(CASE WHEN energy_metric='fossil_fuel_consumption' THEN energy_amount END) AS fossil_fuel_consumption,
  SUM(CASE WHEN energy_metric='fossil_cons_change_pct' THEN energy_amount END) AS fossil_cons_change_pct,
  SUM(CASE WHEN energy_metric='fossil_cons_change_twh' THEN energy_amount END) AS fossil_cons_change_twh,
  SUM(CASE WHEN energy_metric='fossil_cons_per_capita' THEN energy_amount END) AS fossil_cons_per_capita,
  SUM(CASE WHEN energy_metric='fossil_electricity' THEN energy_amount END) AS fossil_electricity,
  SUM(CASE WHEN energy_metric='fossil_energy_per_capita' THEN energy_amount END) AS fossil_energy_per_capita,
  SUM(CASE WHEN energy_metric='fossil_share_elec' THEN energy_amount END) AS fossil_share_elec,
  SUM(CASE WHEN energy_metric='fossil_share_energy' THEN energy_amount END) AS fossil_share_energy,
  SUM(CASE WHEN energy_metric='biofuel_consumption' THEN energy_amount END) AS biofuel_consumption,
  SUM(CASE WHEN energy_metric='biofuel_cons_change_pct' THEN energy_amount END) AS biofuel_cons_change_pct,
  SUM(CASE WHEN energy_metric='biofuel_cons_change_twh' THEN energy_amount END) AS biofuel_cons_change_twh,
  SUM(CASE WHEN energy_metric='biofuel_cons_per_capita' THEN energy_amount END) AS biofuel_cons_per_capita,
  SUM(CASE WHEN energy_metric='biofuel_electricity' THEN energy_amount END) AS biofuel_electricity,
  SUM(CASE WHEN energy_metric='biofuel_elec_per_capita' THEN energy_amount END) AS biofuel_elec_per_capita,
  SUM(CASE WHEN energy_metric='biofuel_share_elec' THEN energy_amount END) AS biofuel_share_elec,
  SUM(CASE WHEN energy_metric='biofuel_share_energy' THEN energy_amount END) AS biofuel_share_energy,
  SUM(CASE WHEN energy_metric='low_carbon_consumption' THEN energy_amount END) AS low_carbon_consumption,
  SUM(CASE WHEN energy_metric='low_carbon_cons_change_pct' THEN energy_amount END) AS low_carbon_cons_change_pct,
  SUM(CASE WHEN energy_metric='low_carbon_cons_change_twh' THEN energy_amount END) AS low_carbon_cons_change_twh,
  SUM(CASE WHEN energy_metric='low_carbon_electricity' THEN energy_amount END) AS low_carbon_electricity,
  SUM(CASE WHEN energy_metric='low_carbon_elec_per_capita' THEN energy_amount END) AS low_carbon_elec_per_capita,
  SUM(CASE WHEN energy_metric='low_carbon_share_elec' THEN energy_amount END) AS low_carbon_share_elec,
  SUM(CASE WHEN energy_metric='low_carbon_share_energy' THEN energy_amount END) AS low_carbon_share_energy,
  SUM(CASE WHEN energy_metric='nuclear_consumption' THEN energy_amount END) AS nuclear_consumption,
  SUM(CASE WHEN energy_metric='nuclear_cons_change_pct' THEN energy_amount END) AS nuclear_cons_change_pct,
  SUM(CASE WHEN energy_metric='nuclear_cons_change_twh' THEN energy_amount END) AS nuclear_cons_change_twh,
  SUM(CASE WHEN energy_metric='nuclear_electricity' THEN energy_amount END) AS nuclear_electricity,
  SUM(CASE WHEN energy_metric='nuclear_elec_per_capita' THEN energy_amount END) AS nuclear_elec_per_capita,
  SUM(CASE WHEN energy_metric='nuclear_energy_per_capita' THEN energy_amount END) AS nuclear_energy_per_capita,
  SUM(CASE WHEN energy_metric='nuclear_share_elec' THEN energy_amount END) AS nuclear_share_elec,
  SUM(CASE WHEN energy_metric='nuclear_share_energy' THEN energy_amount END) AS nuclear_share_energy,
  SUM(CASE WHEN energy_metric='wind_consumption' THEN energy_amount END) AS wind_consumption,
  SUM(CASE WHEN energy_metric='wind_cons_change_pct' THEN energy_amount END) AS wind_cons_change_pct,
  SUM(CASE WHEN energy_metric='wind_cons_change_twh' THEN energy_amount END) AS wind_cons_change_twh,
  SUM(CASE WHEN energy_metric='wind_electricity' THEN energy_amount END) AS wind_electricity,
  SUM(CASE WHEN energy_metric='wind_elec_per_capita' THEN energy_amount END) AS wind_elec_per_capita,
  SUM(CASE WHEN energy_metric='wind_energy_per_capita' THEN energy_amount END) AS wind_energy_per_capita,
  SUM(CASE WHEN energy_metric='wind_share_elec' THEN energy_amount END) AS wind_share_elec,
  SUM(CASE WHEN energy_metric='wind_share_energy' THEN energy_amount END) AS wind_share_energy,
  SUM(CASE WHEN energy_metric='solar_consumption' THEN energy_amount END) AS solar_consumption,
  SUM(CASE WHEN energy_metric='solar_cons_change_pct' THEN energy_amount END) AS solar_cons_change_pct,
  SUM(CASE WHEN energy_metric='solar_cons_change_twh' THEN energy_amount END) AS solar_cons_change_twh,
  SUM(CASE WHEN energy_metric='solar_electricity' THEN energy_amount END) AS solar_electricity,
  SUM(CASE WHEN energy_metric='solar_elec_per_capita' THEN energy_amount END) AS solar_elec_per_capita,
  SUM(CASE WHEN energy_metric='solar_energy_per_capita' THEN energy_amount END) AS solar_energy_per_capita,
  SUM(CASE WHEN energy_metric='solar_share_elec' THEN energy_amount END) AS solar_share_elec,
  SUM(CASE WHEN energy_metric='solar_share_energy' THEN energy_amount END) AS solar_share_energy,
  SUM(CASE WHEN energy_metric='hydro_consumption' THEN energy_amount END) AS hydro_consumption,
  SUM(CASE WHEN energy_metric='hydro_cons_change_pct' THEN energy_amount END) AS hydro_cons_change_pct,
  SUM(CASE WHEN energy_metric='hydro_cons_change_twh' THEN energy_amount END) AS hydro_cons_change_twh,
  SUM(CASE WHEN energy_metric='hydro_electricity' THEN energy_amount END) AS hydro_electricity,
  SUM(CASE WHEN energy_metric='hydro_elec_per_capita' THEN energy_amount END) AS hydro_elec_per_capita,
  SUM(CASE WHEN energy_metric='hydro_energy_per_capita' THEN energy_amount END) AS hydro_energy_per_capita,
  SUM(CASE WHEN energy_metric='hydro_share_elec' THEN energy_amount END) AS hydro_share_elec,
  SUM(CASE WHEN energy_metric='hydro_share_energy' THEN energy_amount END) AS hydro_share_energy,
  SUM(CASE WHEN energy_metric='renewables_consumption' THEN energy_amount END) AS renewables_consumption,
  SUM(CASE WHEN energy_metric='renewables_cons_change_pct' THEN energy_amount END) AS renewables_cons_change_pct,
  SUM(CASE WHEN energy_metric='renewables_electricity' THEN energy_amount END) AS renewables_electricity,
  SUM(CASE WHEN energy_metric='renewables_elec_per_capita' THEN energy_amount END) AS renewables_elec_per_capita,
  SUM(CASE WHEN energy_metric='renewables_energy_per_capita' THEN energy_amount END) AS renewables_energy_per_capita,
  SUM(CASE WHEN energy_metric='renewables_share_energy' THEN energy_amount END) AS renewables_share_energy,
  SUM(CASE WHEN energy_metric='renewables_share_elec' THEN energy_amount END) AS renewables_share_elec,
  SUM(CASE WHEN energy_metric='other_renewables_consumption' THEN energy_amount END) AS other_renewables_consumption,
  SUM(CASE WHEN energy_metric='other_renewables_cons_change_pct' THEN energy_amount END) AS other_renewables_cons_change_pct,
  SUM(CASE WHEN energy_metric='other_renewables_cons_change_twh' THEN energy_amount END) AS other_renewables_cons_change_twh,
  SUM(CASE WHEN energy_metric='other_renewables_electricity' THEN energy_amount END) AS other_renewables_electricity,
  SUM(CASE WHEN energy_metric='other_renewables_elec_per_capita' THEN energy_amount END) AS other_renewables_elec_per_capita,
  SUM(CASE WHEN energy_metric='other_renewables_energy_per_capita' THEN energy_amount END) AS other_renewables_energy_per_capita,
  SUM(CASE WHEN energy_metric='other_renewables_share_elec' THEN energy_amount END) AS other_renewables_share_elec,
  SUM(CASE WHEN energy_metric='other_renewables_share_energy' THEN energy_amount END) AS other_renewables_share_energy,
  SUM(CASE WHEN energy_metric='other_renewables_electricity_exc_biofuel' THEN energy_amount END) AS other_renewables_electricity_exc_biofuel,
  SUM(CASE WHEN energy_metric='other_renewables_elec_per_capita_exc_biofuel' THEN energy_amount END) AS other_renewables_elec_per_capita_exc_biofuel,
  SUM(CASE WHEN energy_metric='other_renewables_share_elec_exc_biofuel' THEN energy_amount END) AS other_renewables_share_elec_exc_biofuel,
  SUM(CASE WHEN energy_metric='primary_energy_consumption' THEN energy_amount END) AS primary_energy_consumption,
  SUM(CASE WHEN energy_metric='energy_cons_change_pct' THEN energy_amount END) AS energy_cons_change_pct,
  SUM(CASE WHEN energy_metric='energy_cons_change_twh' THEN energy_amount END) AS energy_cons_change_twh,
  SUM(CASE WHEN energy_metric='per_capita_electricity' THEN energy_amount END) AS per_capita_electricity,
  SUM(CASE WHEN energy_metric='energy_per_capita' THEN energy_amount END) AS energy_per_capita,
  SUM(CASE WHEN energy_metric='energy_per_gdp' THEN energy_amount END) AS energy_per_gdp
  FROM
  staging_energy
  GROUP BY iso_code, country, year, population, gdp
  )

SELECT da.date_id, co.country_id, AVG(te.average_temp) AS temperature, 
em.co2_emissions, em.ch4_emissions, em.n2o_emissions, en.population, 
en.gdp, en.coal_production, en.coal_prod_change_pct, 
en.coal_prod_change_twh, en.coal_prod_per_capita, en.coal_consumption, 
en.coal_cons_change_pct, en.coal_cons_change_twh, 
en.coal_cons_per_capita, en.coal_electricity, en.coal_elec_per_capita, 
en.coal_share_elec, en.coal_share_energy, en.oil_production, 
en.oil_prod_change_pct, en.oil_prod_change_twh, en.oil_prod_per_capita, 
en.oil_consumption, en.oil_cons_change_pct, en.oil_cons_change_twh, 
en.oil_electricity, en.oil_elec_per_capita, en.oil_energy_per_capita, 
en.oil_share_elec, en.oil_share_energy, en.gas_production, 
en.gas_prod_change_pct, en.gas_prod_change_twh, en.gas_prod_per_capita, 
en.gas_consumption, en.gas_cons_change_pct, en.gas_cons_change_twh, 
en.gas_electricity, en.gas_elec_per_capita, en.gas_energy_per_capita, 
en.gas_share_elec, en.gas_share_energy, en.fossil_fuel_consumption, 
en.fossil_cons_change_pct, en.fossil_cons_change_twh, 
en.fossil_cons_per_capita, en.fossil_electricity, 
en.fossil_energy_per_capita, en.fossil_share_elec, 
en.fossil_share_energy, en.biofuel_consumption, 
en.biofuel_cons_change_pct, en.biofuel_cons_change_twh, 
en.biofuel_cons_per_capita, en.biofuel_electricity, 
en.biofuel_elec_per_capita, en.biofuel_share_elec, 
en.biofuel_share_energy, en.low_carbon_consumption, 
en.low_carbon_cons_change_pct, en.low_carbon_cons_change_twh, 
en.low_carbon_electricity, en.low_carbon_elec_per_capita, 
en.low_carbon_share_elec, en.low_carbon_share_energy, 
en.nuclear_consumption, en.nuclear_cons_change_pct, 
en.nuclear_cons_change_twh, en.nuclear_electricity, 
en.nuclear_elec_per_capita, en.nuclear_energy_per_capita, 
en.nuclear_share_elec, en.nuclear_share_energy, en.wind_consumption, 
en.wind_cons_change_pct, en.wind_cons_change_twh, en.wind_electricity, 
en.wind_elec_per_capita, en.wind_energy_per_capita, en.wind_share_elec, 
en.wind_share_energy, en.solar_consumption, en.solar_cons_change_pct, 
en.solar_cons_change_twh, en.solar_electricity, 
en.solar_elec_per_capita, en.solar_energy_per_capita, 
en.solar_share_elec, en.solar_share_energy, en.hydro_consumption, 
en.hydro_cons_change_pct, en.hydro_cons_change_twh, 
en.hydro_electricity, en.hydro_elec_per_capita, 
en.hydro_energy_per_capita, en.hydro_share_elec, 
en.hydro_share_energy, en.renewables_consumption, 
en.renewables_cons_change_pct, en.renewables_electricity, 
en.renewables_elec_per_capita, en.renewables_energy_per_capita, 
en.renewables_share_energy, en.renewables_share_elec, 
en.other_renewables_consumption, en.other_renewables_cons_change_pct, 
en.other_renewables_cons_change_twh, en.other_renewables_electricity, 
en.other_renewables_elec_per_capita, 
en.other_renewables_energy_per_capita, en.other_renewables_share_elec, 
en.other_renewables_share_energy, 
en.other_renewables_electricity_exc_biofuel, 
en.other_renewables_elec_per_capita_exc_biofuel, 
en.other_renewables_share_elec_exc_biofuel, 
en.primary_energy_consumption, en.energy_cons_change_pct, 
en.energy_cons_change_twh, en.per_capita_electricity, 
en.energy_per_capita, en.energy_per_gdp

FROM staging_temp te
INNER JOIN date da 
	ON EXTRACT(year FROM te.dt) = da.year
INNER JOIN country co 
	ON te.country = co.name
INNER JOIN emissions em
	ON da.year = em.year 
    	AND co.iso_code = em.iso_code
INNER JOIN energy en
	ON da.year = en.year
    	AND co.name = en.country
        AND co.iso_code = en.iso_code
GROUP BY date_id, country_id, en.population, en.gdp, em.co2_emissions, 
em.ch4_emissions, em.n2o_emissions, en.coal_production, 
en.coal_prod_change_pct, en.coal_prod_change_twh, 
en.coal_prod_per_capita, en.coal_consumption, en.coal_cons_change_pct, 
en.coal_cons_change_twh, en.coal_cons_per_capita, en.coal_electricity, 
en.coal_elec_per_capita, en.coal_share_elec, en.coal_share_energy, 
en.oil_production, en.oil_prod_change_pct, en.oil_prod_change_twh, 
en.oil_prod_per_capita, en.oil_consumption, en.oil_cons_change_pct, 
en.oil_cons_change_twh, en.oil_electricity, en.oil_elec_per_capita, 
en.oil_energy_per_capita, en.oil_share_elec, en.oil_share_energy, 
en.gas_production, en.gas_prod_change_pct, en.gas_prod_change_twh, 
en.gas_prod_per_capita, en.gas_consumption, en.gas_cons_change_pct, 
en.gas_cons_change_twh, en.gas_electricity, en.gas_elec_per_capita, 
en.gas_energy_per_capita, en.gas_share_elec, en.gas_share_energy, 
en.fossil_fuel_consumption, en.fossil_cons_change_pct, 
en.fossil_cons_change_twh, en.fossil_cons_per_capita, 
en.fossil_electricity, en.fossil_energy_per_capita, 
en.fossil_share_elec, en.fossil_share_energy, en.biofuel_consumption, 
en.biofuel_cons_change_pct, en.biofuel_cons_change_twh, 
en.biofuel_cons_per_capita, en.biofuel_electricity, 
en.biofuel_elec_per_capita, en.biofuel_share_elec, 
en.biofuel_share_energy, en.low_carbon_consumption, 
en.low_carbon_cons_change_pct, en.low_carbon_cons_change_twh, 
en.low_carbon_electricity, en.low_carbon_elec_per_capita, 
en.low_carbon_share_elec, en.low_carbon_share_energy,
en.nuclear_consumption, en.nuclear_cons_change_pct, 
en.nuclear_cons_change_twh, en.nuclear_electricity, 
en.nuclear_elec_per_capita, en.nuclear_energy_per_capita, 
en.nuclear_share_elec, en.nuclear_share_energy, en.wind_consumption, 
en.wind_cons_change_pct, en.wind_cons_change_twh, en.wind_electricity, 
en.wind_elec_per_capita, en.wind_energy_per_capita, en.wind_share_elec, 
en.wind_share_energy, en.solar_consumption, en.solar_cons_change_pct, 
en.solar_cons_change_twh, en.solar_electricity, 
en.solar_elec_per_capita, en.solar_energy_per_capita, 
en.solar_share_elec, en.solar_share_energy, en.hydro_consumption, 
en.hydro_cons_change_pct, en.hydro_cons_change_twh, 
en.hydro_electricity, en.hydro_elec_per_capita, 
en.hydro_energy_per_capita, en.hydro_share_elec, en.hydro_share_energy, 
en.renewables_consumption, en.renewables_cons_change_pct, 
en.renewables_electricity, en.renewables_elec_per_capita, 
en.renewables_energy_per_capita, en.renewables_share_energy, 
en.renewables_share_elec, en.other_renewables_consumption, 
en.other_renewables_cons_change_pct, 
en.other_renewables_cons_change_twh, en.other_renewables_electricity, 
en.other_renewables_elec_per_capita, 
en.other_renewables_energy_per_capita, en.other_renewables_share_elec, 
en.other_renewables_share_energy, 
en.other_renewables_electricity_exc_biofuel, 
en.other_renewables_elec_per_capita_exc_biofuel, 
en.other_renewables_share_elec_exc_biofuel, 
en.primary_energy_consumption, en.energy_cons_change_pct, 
en.energy_cons_change_twh, en.per_capita_electricity, 
en.energy_per_capita, en.energy_per_gdp
""")


# QUERY LIST

create_table_queries = [staging_temp_table_create, 
            staging_emissions_table_create, staging_energy_table_create, 
            date_table_create, country_table_create, fact_table_create]

drop_table_queries = [staging_temp_table_drop, 
            staging_emissions_table_drop, staging_energy_table_drop, 
            date_table_drop, country_table_drop, fact_table_drop]

copy_table_queries = [staging_temp_copy, staging_emissions_copy, 
            staging_energy_copy]

insert_table_queries = [country_table_insert, date_table_insert, 
            fact_table_insert]