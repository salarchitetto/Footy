import pandas as pd

def grab_data(conn, country=None):
    """

    :param conn: connection used to get into footy db
    :param country: add a country value to splice the df
    :return: pandas dataframe
    """
    matches = """

        SELECT *
        FROM footy_matches
    """
    if country is not None:
        matches = matches + "WHERE country IN ('" + str(country) + "')"

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
