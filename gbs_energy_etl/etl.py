import psycopg2
from gbs_energy_etl.sql_queries import copy_table_queries, insert_table_queries
from gbs_energy_etl.settings import config


def load_staging_tables(cur, conn):
    """
     - load data from S3 to staging in Redshift
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_final_tables(cur, conn):
    """
     - insert from staging to final tables
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
     - connect to Redshift
     - stage tables
     - produce final tables
    """
    conn = psycopg2.connect('user={} password={} host={}\
                            port={} dbname={}'
                            .format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_final_tables(cur, conn)
    conn.close()


if __name__ == '__main__':
    main()
