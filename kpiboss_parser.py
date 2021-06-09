import json
import csv
import os

#GLOBAL CONSTANTS
OUTPUT_FOLDER = "output"
FILENAME = "t.json"
FIELDNAMES = ['KPI Description', 'KPI Name', 'Actions', 'OID', 'Normalize', 'Source']


# USE THIS FORMAT LATER TO WRITE INTO THE CSV FILE
# To add multiple items into the same cell we need to join them into a str
# Example: ["name1", "name2"] : list --> ','.join(["name1", "name2"])

# data = {
#         'KPI Description': "test Description",
#         'KPI Name': "test Name",
#         'Actions': "test Actions",
#         'OID': "test OID",
#         'Normalize': "test NOMALIZE",
#         'Source': "test SOURCE",
#             }

def get_data(parameter):
    """
    Recieves the parameters, gets all data needed, makes a dict and return it
    :param parameter: dict
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

    if 'name_' in parameter:
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
    filename = collection_mode['name_']
    parameters = collection_mode['parameters']

    if not filename.endswith(".csv"):
        filename += ".csv"

    file_path = os.path.join(OUTPUT_FOLDER, filename)

    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for parameter in parameters:
            data = get_data(parameter)
            writer.writerow(data)


def main():
    """
    Function main, loads necessary json data and for each collection_mode,
    calls the write_into_csv_file method and generates a csv file

    :return:
    """
    with open(FILENAME, "r") as data_file:
        data = json.load(data_file)
        collection_modes = data['collection_modes']
        for collection_mode in collection_modes:
            write_into_csv_file(collection_mode)


if __name__ == '__main__':
    main()
