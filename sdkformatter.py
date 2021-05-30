import vdf
import os
import json
from bitbakedataserializer import load_bitbake_data


def app_build_setup():
    from plasticscm import current_changeset

    bitbake_data = load_bitbake_data()
    output_dir = bitbake_data[0]['SteamSDKDirectory'] + "/tools/ContentBuilder/output"
    appid = bitbake_data[0]['AppID']
    steam_branch = bitbake_data[0]['SteamBranch']

    description = "Current Changeset: {}".format(current_changeset())

    builder_vdf = vdf.load(open('{}/generic_app_build.vdf'.format(os.path.dirname(__file__)), 'r'))
    depot_vdf = os.getcwd()

    # Writes all values to the App Build VDF
    builder_vdf['appbuild']['appid'] = appid
    builder_vdf['appbuild']['desc'] = description
    builder_vdf['appbuild']['buildoutput'] = output_dir
    builder_vdf['appbuild']['setlive'] = steam_branch

    # Deletes all current depots to add new ones
    builder_vdf['appbuild']['depots'].clear()

    # Hack to increase app id by 1, assuming the base Steam Depots are always AppID + 1
    # TODO: Add support for more than 1 depot
    depot_key = int(appid) + 1
    builder_vdf['appbuild']['depots'][str(depot_key)] = depot_vdf + "\custom_depot.vdf"

    # Temporarily dumps users parameters on a VDF
    with open('{}/custom_app_build.vdf'.format(os.path.dirname(__file__)), 'w+') as in_file:
        in_file.truncate()
        vdf.dump(builder_vdf, in_file, pretty=True)

    # Reopens the VDF so its contents are recorded and edits out all \\ from the code
    # This is only needed because stupid VDF Library doesn't dump Paths with regular \ notation
    with open('custom_app_build.vdf', 'r+') as out_file:
        all_lines = []
        for line in out_file:
            line = line.replace(r'\\', '\\')
            all_lines.append(line)
        out_file.seek(0)
        out_file.truncate()
        out_file.writelines(all_lines)


def depot_setup(build_folder):

    bitbake_data = load_bitbake_data()
    depot_id = bitbake_data[0]['AppID']
    build_dir = bitbake_data[0]['BuildDirectory']
    depot_vdf = vdf.load(open('{}/generic_depot.vdf'.format(os.path.dirname(__file__)), 'r'))

    # Writes all values to the Depot VDF
    depot_id = int(depot_id) + 1
    depot_vdf['DepotBuildConfig']['DepotID'] = str(depot_id)
    depot_vdf['DepotBuildConfig']['contentroot'] = "{}/{}".format(build_dir, build_folder)

    # Temporarily dumps users parameters on a VDF
    with open('{}/custom_depot.vdf'.format(os.path.dirname(__file__)), 'w+') as in_file:
        in_file.truncate()
        vdf.dump(depot_vdf, in_file, pretty=True)


def upload_to_steam(folder_name):
    import subprocess

    app_build_setup()
    depot_setup(folder_name)

    data_dir = os.path.dirname(__file__)
    data_file = open('{}/generic_projectdata.json'.format(data_dir), 'r')
    bake_data = json.load(data_file)

    steam_cmd = bake_data[0]['SteamSDKDirectory'] + "/tools/ContentBuilder/builder/steamcmd.exe"
    login = bake_data[0]['SteamLogin']
    password = bake_data[0]['SteamPassword']
    vdf_file = '{}/custom_app_build.vdf'.format(data_dir)

    upload_config = subprocess.run([steam_cmd,
                                    '+login',
                                    login,
                                    password,
                                    '+run_app_build',
                                    vdf_file,
                                    '+quit',
                                    ])

    print("Process Finished and Build Uploaded")

    return upload_config.returncode


if __name__ == '__main__':
    app_build_setup()
    # depot_setup('210520_NekoNeko')
    # print("*" * 40)
    # depot_setup("210515_NekoNeko")
    # upload_to_steam("210515_NekoNeko")