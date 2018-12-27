import pandas as pd
import numpy as np
import os

def footy_colors(color, type='html'):
    """

    :param color:
    :param type:
    :return:
    """

    colors = {'MAASTRICHT BLUE': {'html':'#0B132B'},
              'YANKEES BLUE': {'html':'#1C2541'},
              'INDEPENDENCE': {'html':'#3A506B'},
              'SEA SERPENT': {'html':'#5BC0BE'},
              'AQUAMARINE': {'html':'#6FFFE9'},
              'MIDNIGHT GREEN': {'html':'#114B5F'},
              'ILLUMINATING EMERALD': {'html':'#1A936F'}}


    return colors[color][type]
