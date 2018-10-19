import pandas as pd
from scrape_data.create_db import *

conn = create_connection()

def grab_data(conn):
    """

    :param conn: connection used to get into footy db
    :return: pandas dataframe
    """

    matches = """
        SELECT *
        FROM matches
    """

    df = pd.read_sql(matches, conn)

    return df


