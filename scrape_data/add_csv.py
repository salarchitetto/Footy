import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np
import os

from scrape_data.create_db import  *
#"C:\\Users\\Sal Architetto\\PycharmProjects\\footy\\database\\footy.db"


conn = create_connection()

def loop_file_locations():
    pass