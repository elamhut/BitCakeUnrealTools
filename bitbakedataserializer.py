import os
import sys
import json


def load_bitbake_data():
    data_dir = os.path.dirname(__file__)
    data_file = open("{}/generic_projectdata.json".format(data_dir), 'r')
    bake_data = json.load(data_file)

    return bake_data


def data_serialize(in_data):
    # Open Project JSON to Edit
    json_dir = os.path.dirname(__file__)
    json_file = open('{}/generic_projectdata.json'.format(json_dir), 'r+')
    project_json = json.load(json_file)

    # Get Argument, split it into Key and Value and use the Key to find and replace the new Data inside the JSON
    split_data = in_data.split("|")
    project_json[0][split_data[0]] = split_data[1]

    # Move Carat to the start of the file, delete everything than write the new data
    json_file.seek(0)
    json_file.truncate()
    json_file.write(json.dumps(project_json, indent=4))
    json_file.close()


if __name__ == '__main__':
    bitdata = str(sys.argv[1])
    data_serialize(bitdata)