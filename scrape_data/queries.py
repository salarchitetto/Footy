import pandas as pd
import os

try:
    import MySQLdb
except:
    import pymysql

    pymysql.install_as_MySQLdb()
    import MySQLdb


def footy_connect(host=eval(os.environ['FOOTY_CRED'])['host'],
                  user=eval(os.environ['FOOTY_CRED'])['user'],
                  passwd=eval(os.environ['FOOTY_CRED'])['passwd'],
                  dbName=eval(os.environ['FOOTY_CRED'])['db']):
    footy_conn = MySQLdb.connect(
        host=host,
        user=user,
        passwd=passwd,
        db=dbName
    )
    print("Conection Made")
    return footy_conn


def kaggle_connect(host=eval(os.environ['KAGGLE_CRED'])['host'],
                   user=eval(os.environ['KAGGLE_CRED'])['user'],
                   passwd=eval(os.environ['KAGGLE_CRED'])['passwd'],
                   dbName=eval(os.environ['KAGGLE_CRED'])['db']):
    kaggle_conn = MySQLdb.connect(
        host=host,
        user=user,
        passwd=passwd,
        db=dbName
    )
    print('Connection Made')
    return kaggle_conn


def grab_data(conn, country=None, team_name=None, division=None):
    """

    :param conn: connection used to get into footy db
    :param country: add a country value to splice the df
    :return: pandas dataframe
    """
    matches = """

        SELECT *
        FROM footy_data
        WHERE home_team != '0'
    """
    if country is not None:
        matches = matches + " AND country IN ('" + str(country) + "')"

    df = pd.read_sql(matches, conn)

    return df


def grab_team_names(conn, division=None, country=None):
    """

    :param conn:
    :param country:
    :return:
    """

    names = """
        SELECT DISTINCT home_team,
        dates
        FROM footy_data
     """

    if country is not None:
        names = names + "WHERE division IN ('" + str(country) + "')"

    if division is not None:
        names = names + " AND country IN ('" + str(division) + "')"

    names = names + " AND home_team != '0' ORDER BY home_team ASC"

    df = pd.read_sql(names, conn)

    return df


def grab_divisions(conn, country=None):
    division = """

        SELECT DISTINCT division
        FROM footy_data
    """

    if country is not None:
        division = division + " WHERE country IN ('" + str(country) + "')"

    division = division + " ORDER BY division ASC"

    df = pd.read_sql_query(division, conn)

    return df


