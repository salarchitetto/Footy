import pandas as pd
import glob
import os

def read_dir(directory):
    """
    loop through a directory to get a specific
    csv path
    :param directory: initial strarting directory
    :return: list of csv directories
    """
    files = os.listdir(directory)
    file_path = []

    for x in files:
        file_path.append(directory + "\\" + x)

    return file_path

def remove_null_values(csv, country):
    """
    Function to remove all '' (empty data) from csv
    :param csv: directory pointer to csv
    :return: rewritten data to file
    """

    for x in csv:
        print(x)
        try:
            read_csv = pd.read_csv(x, error_bad_lines=False, encoding='cp1252')
        except:
            read_csv = x.encode('utf-8').strip()
            read_csv = pd.read_csv(x, error_bad_lines=False,encoding='cp1252')

        print(read_csv.head(5))
        modified_csv = read_csv.fillna(0)

        modified_csv["country"] = country

        check = modified_csv.isnull().sum().sum()
        print(check)

        if check > 0:
            print("Error: still '' values")
        else:
            print("There is no '' values")

        #resaving to csv
        modified_csv.to_csv(x)
