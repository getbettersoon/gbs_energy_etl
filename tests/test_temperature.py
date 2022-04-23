import unittest
import psycopg2
from gbs_energy_etl.settings import config


conn = psycopg2.connect("user={} password={} host={} port={} dbname={}"
                        .format(*config['CLUSTER'].values()))
cur = conn.cursor()


class TestTemperature(unittest.TestCase):
    def test_temperature(self):
        """
        - Compare average temperature by country by year between
          staging_temp and fact table
        """

        # define variables for testing
        countries = ('Poland', 'Canada', 'Chad', 'Japan')
        year = 2013

        # run query against source dataset
        cur.execute(f"""
            SELECT EXTRACT(year from dt) as year, country,
                AVG(average_temp)
            FROM staging_temp
            WHERE country IN {countries}
                AND year = {year}
            GROUP BY year, country
            ORDER BY country
        """)

        print('\nSTAGING:')
        staging_result = []
        for row in cur.fetchall():
            print(f'Temperature in {row[0]} in {row[1]} was {row[2]}')
            staging_result.append(float(row[2]))

        # run query against fact table
        cur.execute(f"""
            SELECT da.year, co.name, temperature
            FROM fact f
            JOIN date da ON f.date_id = da.date_id
            JOIN country co ON f.country_id = co.country_id
            WHERE co.name IN {countries}
            AND year = {year}
            ORDER BY co.name
        """)

        fact_result = []
        print('\nFACTS:')
        for row in cur.fetchall():
            print(f'Temperature in {row[0]} in {row[1]} was {row[2]}')
            fact_result.append(float(row[2]))

        self.assertEqual(staging_result, fact_result)


if __name__ == '__main__':
    unittest.main()
