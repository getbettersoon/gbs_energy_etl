import logging
import psycopg2
from gbs_energy_etl.settings import config
from gbs_energy_etl.etl import (execute_tables, insert_final_tables,
                                load_staging_tables)
from gbs_energy_etl.sql_queries import (execute_table_queries,
                                        copy_table_queries,
                                        insert_table_queries)


def main():
    """
     - creates connection to Redshift

     - drops and creates all tables
    """
    conn = psycopg2.connect('user={} password={} host={}\
                            port={} dbname={}'
                            .format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    # clean_data()
    execute_tables(cur, conn, execute_table_queries)
    load_staging_tables(cur, conn, copy_table_queries)
    insert_final_tables(cur, conn, insert_table_queries)
    conn.close()


if __name__ == '__main__':
    main()
