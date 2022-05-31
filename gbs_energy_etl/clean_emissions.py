import awswrangler as wr
import pandas as pd
import numpy as np


def clean_emissions(config):
    """
     - download dataset from S3, clean and upload to S3
    """

    BUCKET = config['S3']['BUCKET']

    df = wr.s3.read_csv(f"s3://{BUCKET}"
                        + "/CW_HistoricalEmissions_PIK.csv")

    # rename column
    df = df.rename(columns={'country': 'iso_code'})

    # keep total emissions only, remove individual sectors
    filt_sectors = df['sector'] == 'Total excluding LULUCF'
    df = df[filt_sectors]

    # drop 'source' column
    df = df.drop(labels=['source', 'unit', 'sector'], axis=1)

    # remove non-countries
    iso_filter = df['iso_code'].str.len() == 3
    df = df[iso_filter]

    # drop rows with majority of missing values
    df = df.replace({'#NUM!': np.nan}).dropna(thresh=150)

    # convert columns into rows
    all_country_columns = list(map(str, range(1850, 2019)))
    df = pd.melt(df, id_vars=['iso_code', 'gas'],
                value_vars=all_country_columns,
                var_name='year',
                value_name='emission_amount')

    wr.s3.to_csv(df,
                f"s3://{BUCKET}/clean_CW_HistoricalEmissions_PIK.csv",
                index=False)
