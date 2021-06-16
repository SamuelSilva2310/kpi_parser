"""
Author: Samuel Silva
Date: 9/06/2021

This the main file of the parser. This Script loads a .json file
and for each collection_mode it generates a .csv file

The format of columns are:
        - ['KPI Description', 'KPI Name', 'Actions', 'OID', 'Normalize', 'Source']

The way items are written into the .csv file is by giving the writer object a dict:
        -  {
            'KPI Description': kpi_description,
            'KPI Name': kpi_name,
            'Actions': kpi_action,
            'OID': kpi_oid,
            'Normalize': kpi_normalize,
            'Source': kpi_source
            }
"""
import ast
import json

import commentjson
import csv
import os

# GLOBAL CONSTANTS
OUTPUT_FOLDER = "output"
FILENAME = "parsed.json"
FIELDNAMES = ['KPI Description', 'KPI Name', 'Actions', 'OID', 'Normalize', 'Source']


def get_data(parameter, name=None):
    """
    Recieves the parameters when its a list and also a name when its a dict, gets all data needed,
    creates a proper dict which will be used as the row for the csv file and returns it.

    :param parameter: dict
    :param name: str
    :return: dict -> data
    """

    kpi_description = ""
    kpi_name = ""
    kpi_action = ""
    kpi_oid = ""
    kpi_normalize = ""
    kpi_source = ""

    if 'description' in parameter:
        description = parameter['description']

    if name:
        kpi_name = name
    elif 'name_' in parameter:
        kpi_name = parameter['name_']

    if 'action' in parameter:
        kpi_action = parameter['action']

    if 'tr_value_long' in parameter:
        kpi_oid = parameter['tr_value_long']
    elif 'oid' in parameter:
        kpi_oid = parameter['oid']

    if 'normalize' in parameter:
        kpi_normalize = parameter['normalize']

    if 'source' in parameter:
        kpi_source = parameter['source']

    if isinstance(kpi_action, list):
        kpi_action = '|'.join(kpi_action)

    data = {
        'KPI Description': kpi_description,
        'KPI Name': kpi_name,
        'Actions': kpi_action,
        'OID': kpi_oid,
        'Normalize': kpi_normalize,
        'Source': kpi_source
    }

    return data


def write_into_csv_file(collection_mode):
    """
    Gets all data and writes into a csv file using a DictWriter
    CSV Writing order -> [KPI Description , KPI Name , Actions , OID , Normalize , Source]

    :parameter collection_mode: list
    :return: None
    """
    filename = collection_mode['name_'] + ".csv"
    file_path = os.path.join(OUTPUT_FOLDER, filename)

    rows = []
    parameters = collection_mode['parameters']

    # If parameters is a list for each item call get_data(item)
    # If parameters is a dict, get all keys and for each key, call get_data() passing the value inside each item,
    # also the get_data(name) parameter will be the key
    if isinstance(parameters, list):
        print(f"[PARAMETERS] Parameters are List file: {filename}")
        for parameter in parameters:
            rows.append(get_data(parameter))
    else:
        print(f"[PARAMETERS] Parameters are Dict file: {filename}")
        for parameter_key in parameters.keys():
            rows.append(get_data(parameters[parameter_key], parameter_key))

    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        print(f"[WRITING] Writing data into file: {filename} \n")

        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    """
    Function main, loads necessary json data and for each collection_mode,
    calls the write_into_csv_file method and generates a csv file

    :return: None
    """
    with open(FILENAME, "r") as data_file:
        print("[LOADING] Loading json data...")
        s = data_file.read()
        data = ast.literal_eval(s)

        print("[LOADED] json data was loaded\n")

        collection_modes = data['collection_modes']

        print("[GENERATING] Generating files...\n")
        for collection_mode in collection_modes:
            write_into_csv_file(collection_mode)


if __name__ == '__main__':
    main()
