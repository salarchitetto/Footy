import os
import pandas as pd
from collections import *
from scrape_data.queries import *
from scrape_data.mysql_connect import *

def choose_team(country_name):
    """
    This function returns a list of the teams per country and will
    populate a drop down in the callbacks
    :param country_name:
    :return: list of team names per country
    """
    #connecting to DB
    conn = footy_connect()

    #grabbing dataframe
    df = grab_team_names(conn, country_name)

    conn.close()

    return df