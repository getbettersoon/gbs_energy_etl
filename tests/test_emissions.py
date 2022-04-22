import unittest
import psycopg2
from gbs_energy_etl.settings import config


conn = psycopg2.connect("user={} password={} host={} port={} dbname={}"
                        .format(*config['CLUSTER'].values()))
cur = conn.cursor()


class TestEmissions(unittest.TestCase):
    def test_emissions(self):
        """
         - compare emission values between staging and fact table
        """
        # define variables for testing
        countries = "('Poland', 'Germany')"
        year = 1989
        gas = "CO2"
        
        # query staging
        cur.execute(f"""
        SELECT year, co.name, gas, emission_amount
        FROM staging_emissions em
        JOIN country co ON em.iso_code = co.iso_code
        WHERE co.name IN {countries}
        AND year = {year}
        AND gas = '{gas}'
        ORDER BY co.name
        """)

        print('\nSTAGING:')
        staging_result = []
        for row in cur.fetchall():
            print(f"{row[2]} emissions in {row[0]} in {row[1]}: {row[3]}")
            staging_result.append(float(row[3]))

        # map type of gas from staging table
        # to respective column name in fact table
        map_gas = {'CO2': 'co2_emissions', 'N2O': 'n2o_emissions',
                   'CH4': 'ch4_emisssions'}
        
        # query fact
        cur.execute(f"""SELECT da.year, co.name, f.{map_gas[gas]}
            FROM fact f
            JOIN date da ON f.date_id = da.date_id
            JOIN country co ON f.country_id = co.country_id
            WHERE co.name IN {countries}
            AND year = {year}
            ORDER BY co.name
        """)

        print('\nFACT:')
        fact_result = []
        for row in cur.fetchall():
            print(f"{gas} emissions in {row[0]} in {row[1]}: {row[2]}")
            fact_result.append(float(row[2]))

        self.assertEqual(staging_result, fact_result)


if __name__ == '__main__':
    unittest.main()