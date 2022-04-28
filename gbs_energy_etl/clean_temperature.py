import awswrangler as wr


def clean_temperature(config):
    """
     - download dataset from S3, clean and upload to S3
    """
    
    df = wr.s3.read_csv(f"s3://gbs-energy/GlobalLandTemperaturesByCountry.csv")

    # drop columns
    df = df.drop(labels=['AverageTemperatureUncertainty'], axis=1)

    # convert column names to snake_case
    df = df.rename(columns=str.lower)\
        .rename(columns=({'averagetemperature':'average_temp'}))

    # correct country names
    df = df.replace(to_replace={
        'Czech Republic':'Czechia',
        'Antigua And Barbuda': 'Antigua and Barbuda',
        'Bosnia And Herzegovina': 'Bosnia and Herzegovina',
        "Côte D'Ivoire":"Côte d'Ivoire",
        'Congo (Democratic Republic Of The)':\
            'Congo (the Democratic Republic of the)',
        'Guinea Bissau':'Guinea-Bissau',
        'Palestina': 'Palestine'})

    BUCKET = config['S3']['BUCKET']
    PREFIX = config['S3']['PREFIX']
    if PREFIX:
        PREFIX = f"/{PREFIX}"

    wr.s3.to_csv(df, f"s3://{BUCKET}{PREFIX}/clean_GlobalLandTemperaturesByCountry.csv", index=False)
