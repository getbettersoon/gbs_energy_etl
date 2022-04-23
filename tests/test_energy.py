import unittest
import psycopg2
from gbs_energy_etl.settings import config


conn = psycopg2.connect("user={} password={} host={} port={} dbname={}"
                        .format(*config['CLUSTER'].values()))
cur = conn.cursor()


class TestEnergy(unittest.TestCase):
    def test_energy(self):
        """
         - compare values between staging_energy dataset and fact table
        """

        # define variables for testing
        countries = ('Poland', 'Germany', 'Spain')
        year = 1989
        emission_metric = 'coal_production'

        # query staging
        cur.execute(f"""
            SELECT year, country, energy_amount
            FROM staging_energy
            WHERE energy_metric = '{emission_metric}'
            AND year = {year}
            AND country IN {countries}
            ORDER BY country
        """)

        print('\nSTAGING:')
        staging_result = []
        for row in cur.fetchall():
            print(f'{emission_metric} in {row[0]} in {row[1]}: {row[2]}')
            staging_result.append(float(row[2]))

        # query fact
        cur.execute(f"""
            SELECT da.year, co.name, {emission_metric} FROM fact f
            JOIN date da ON f.date_id = da.date_id
            JOIN country co ON f.country_id = co.country_id
            WHERE co.name IN {countries}
            AND da.year = {year}
            ORDER BY co.name
        """)

        print('\nFACT:')
        fact_result = []
        for row in cur.fetchall():
            print(f"{emission_metric} in {row[0]} in {row[1]}: {row[2]}")
            fact_result.append(float(row[2]))

        self.assertEqual(staging_result, fact_result)


if __name__ == '__main__':
    unittest.main()
