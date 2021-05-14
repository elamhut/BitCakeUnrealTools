import sys
import json


# bitdata = str(sys.argv[1])


def data_serialize(in_data):
    # Open Project JSON to Edit
    json_file = open('generic_projectdata.json', 'r+')
    project_json = json.load(json_file)

    print(project_json[0])

    split_data = in_data.split(":")
    project_json[0][split_data[0]] = split_data[1]

    print(project_json[0])

    print("*"*40)
    print(json.dumps(project_json[0][split_data[0]]))

    json_file.write(json.dumps(project_json[0], indent=4))
    json_file.close()

if __name__ == '__main__':
    dummydata = 'AppID:987654321'
    data_serialize(dummydata)