import json
import awswrangler as wr
import boto3
import pandas as pd
import numpy as np


def clean_energy(config):
    """
     - download dataset from S3, clean and upload to S3
    """
    # read json from S3 and create df
    s3 = boto3.resource('s3')
    obj = s3.Object('gbs-energy', 'owid-energy-data.json')
    file_content = obj.get()['Body'].read().decode('utf-8')
    data = json.loads(file_content)
    df = pd.DataFrame.from_dict(data, orient='index')\
                    .reset_index()\
                    .rename(columns={'index':'country'})


    # drop non-countries
    df = df.dropna(subset=['iso_code'])

    # iso_codes longer than 3 are regions, not countries
    iso_filter = df['iso_code'].str.len() == 3
    df = df[iso_filter]


    ### flattening data column

    # get a list of countries
    all_countries = df['country'].tolist()

    # get a list of columns and create empty df. Germany has all possible columns
    df_country = pd.json_normalize(data, ['Germany','data'])
    columns = list(df_country.columns)
    columns.insert(0, 'country')
    columns.insert(1, 'iso_code')
    df_final = pd.DataFrame(columns=columns)


    # flatten data for each country, add 'country_name' and 'iso_code' column
    # then concatenate all countries into one df
    for country in all_countries:

        # get iso_code
        filter_iso = df['country'] == country
        iso_code = df[filter_iso]['iso_code'].values[0]

        # flatten data column
        df_flat_country = pd.json_normalize(data, [country,'data'])
        length = df_flat_country.shape[0]

        # create lists with exact number of elements
        country_name_column = [country] * length
        iso_code_column = [iso_code] * length

        # insert elements into new columns
        df_flat_country['country'] = country_name_column
        df_flat_country['iso_code'] = iso_code_column


        df_final = pd.concat([df_final, df_flat_country], ignore_index=True)
        

    # rename inconsistent columns
    df_final = df_final.rename(columns={
        'other_renewable_exc_biofuel_electricity':\
            'other_renewables_electricity_exc_biofuel',
        'other_renewable_consumption': 'other_renewables_consumption',
        'other_renewable_electricity': 'other_renewables_electricity'})

    # correct country names
    df_final = df_final.replace(to_replace={
        'Democratic Republic of Congo':\
            'Congo (the Democratic Republic of the)',
        'Faeroe Islands':'Faroe Islands',
        "Cote d'Ivoire":"Côte d'Ivoire"})

    # move columns into rows
    columns_to_move = list(df_final.columns)[3:]
    columns_to_move.remove('population')
    columns_to_move.remove('gdp')

    df_final = pd.melt(df_final,
                        id_vars=['country', 'iso_code', 'year', 'population', 'gdp'], 
                        value_vars=list(df_final.columns)[3:], 
                        var_name='energy_metric', 
                        value_name='energy_amount')

    # remove outliers
    df_final = df_final.replace(to_replace={np.inf: np.nan})
    df_final.loc[206304, ['energy_amount']] = np.nan

    BUCKET = config['S3']['BUCKET']
    PREFIX = config['S3']['PREFIX']
    if PREFIX:
        PREFIX = f"/{PREFIX}"

    wr.s3.to_json(df_final, f"s3://{BUCKET}{PREFIX}/clean_owid-energy-data.json", orient='records', lines=True)