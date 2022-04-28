import logging
import psycopg2
from gbs_energy_etl.settings import config
from gbs_energy_etl.etl import (execute_tables, 
                                load_staging_tables,
                                insert_final_tables)
from gbs_energy_etl.sql_queries import (execute_table_queries,
                                        copy_table_queries,
                                        insert_table_queries)
from gbs_energy_etl.clean_temperature import clean_temperature
from gbs_energy_etl.clean_energy import clean_energy
from gbs_energy_etl.clean_emissions import clean_emissions


def main():
    """
     - clean datasets
     - create connection to Redshift
     - drop and create all tables
     - load from S3 to Redshift staging
     - load final tables in Redshift
    """
    
    clean_temperature(config)
    clean_energy(config)
    clean_emissions(config)
    

    conn = psycopg2.connect('user={} password={} host={}\
                            port={} dbname={}'
                            .format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    execute_tables(cur, conn, execute_table_queries)
    load_staging_tables(cur, conn, copy_table_queries)
    insert_final_tables(cur, conn, insert_table_queries)

    conn.close()


if __name__ == '__main__':
    main()
