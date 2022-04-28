def execute_tables(cur, conn, queries):
    """
     - drop and create tables
    """
    for query in queries:
        cur.execute(query)
        conn.commit()


def load_staging_tables(cur, conn, queries):
    """
     - load data from S3 to staging in Redshift
    """
    for query in queries:
        cur.execute(query)
        conn.commit()


def insert_final_tables(cur, conn, queries):
    """
     - insert from staging to final tables in Redshift
    """
    for query in queries:
        cur.execute(query)
        conn.commit()
