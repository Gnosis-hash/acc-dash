import psycopg2
import pandas as pd
from config import config

def get_all():
    """ query parts from the parts table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        sql = "SELECT year, degree_type, SUM(loan_amount) AS loan FROM public.main GROUP BY 1, 2;"
        df = pd.read_sql_query(sql, conn)
        ##cur.execute(sql)
        ##rows = cur.fetchall()
        ##print(df)
        return df
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    get_all()