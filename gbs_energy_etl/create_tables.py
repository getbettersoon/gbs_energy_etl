import psycopg2
from gbs_energy_etl.sql_queries import drop_table_queries, create_table_queries
from gbs_energy_etl.settings import config


def drop_tables(conn, cur):
    """
     - drop tables if exist
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(conn, cur):
    """
     - create tables if not exist
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
     - creates connection to Redshift

     - drops and creates all tables
    """
    conn = psycopg2.connect('user={} password={} host={}\
                            port={} dbname={}'
                            .format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(conn, cur)
    create_tables(conn, cur)

    conn.close()


if __name__ == '__main__':
    main()
