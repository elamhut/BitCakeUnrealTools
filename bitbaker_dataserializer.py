import os
import sys
import json


def load_bitbake_data():
    data_dir = os.path.dirname(__file__)
    data_file = open("{}/generic_projectdata.json".format(data_dir), 'r')
    bake_data = json.load(data_file)

    return bake_data


def data_verify():
    data = load_bitbake_data()
    data = data[0].items()

    failed_data = []

    for key, value in data:
        if value == "":
            failed_data.append((key, value))
        else:
            continue

    return failed_data


def data_serialize(key, value):
    # Open Project JSON to Edit
    json_dir = os.path.dirname(__file__)
    json_file = open('{}/generic_projectdata.json'.format(json_dir), 'r+')
    project_json = json.load(json_file)

    project_json[0][key] = value

    # Move Carat to the start of the file, delete everything than write the new data
    json_file.seek(0)
    json_file.truncate()
    json_file.write(json.dumps(project_json, indent=4))
    json_file.close()


if __name__ == '__main__':
    print(data_verify())