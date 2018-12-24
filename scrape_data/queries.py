import pandas as pd
import os
try:
    import MySQLdb
except:
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb

def footy_connect(host=eval(os.environ['CONN_CRED'])['host'],
                  user=eval(os.environ['CONN_CRED'])['user'],
                  passwd=eval(os.environ['CONN_CRED'])['passwd'],
                  dbName=eval(os.environ['CONN_CRED'])['db']):

    footy_connect = MySQLdb.connect(
        host=host,
        user=user,
        passwd=passwd,
        db=dbName
    )
    print("Conection Made")
    return footy_connect

def grab_data(conn, country=None, team_name=None):
    """

    :param conn: connection used to get into footy db
    :param country: add a country value to splice the df
    :return: pandas dataframe
    """
    matches = """

        SELECT *
        FROM footy_matches
        WHERE home_team != '0'
    """
    if country is not None:
        matches = matches + " AND country IN ('" + str(country) + "')"

    df = pd.read_sql(matches, conn)

    return df

def grab_team_names(conn, country=None):
    """

    :param conn:
    :param country:
    :return:
    """
    names = """
        SELECT DISTINCT home_team
        FROM footy_matches
        WHERE home_team != '0'
     """

    if country is not None:
        names = names + "AND country IN ('" + str(country) + "')"
    names = names + " ORDER BY home_team ASC"

    df = pd.read_sql(names, conn)

    return df


