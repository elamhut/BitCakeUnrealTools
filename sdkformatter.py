# Pegar os VDFs e setupar os nomes dos arquivos corretamente
# Montar o run_build.bat corretamente

import vdf
import os


def builder_setup(appid, sdk_dir, build_branch):
    output_dir = sdk_dir + "\\tools\\ContentBuilder\\output"
    builder_vdf = vdf.load(open('generic_app_build.vdf'))
    depot_vdf = os.getcwd()

    # Writes all values to the App Build VDF
    builder_vdf['appbuild']['appid'] = appid
    builder_vdf['appbuild']['buildoutput'] = output_dir
    builder_vdf['appbuild']['setlive'] = build_branch

    # Deletes all current depots to add new ones
    builder_vdf['appbuild']['depots'].clear()
    builder_vdf['appbuild']['depots'][appid] = depot_vdf + "\\custom_depot.vdf"

    # Temporarily dumps users parameters on a VDF
    with open('custom_app_build.vdf', 'w+') as in_file:
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


def depot_setup(appid, build_dir):
    depot_vdf = vdf.load(open('generic_depot.vdf'))

    # Writes all values to the Depot VDF
    depot_vdf['DepotBuildConfig']['DepotID'] = appid
    depot_vdf['DepotBuildConfig']['contentroot'] = build_dir

    # Temporarily dumps users parameters on a VDF
    with open('custom_depot.vdf', 'w+') as in_file:
        in_file.truncate()
        vdf.dump(depot_vdf, in_file, pretty=True)

    # Reopens the VDF so its contents are recorded and edits out all \\ from the code
    # This is only needed because stupid VDF Library doesn't dump Paths with regular \ notation
    with open('custom_depot.vdf', 'r+') as out_file:
        all_lines = []
        for line in out_file:
            line = line.replace(r'\\', '\\')
            all_lines.append(line)
        out_file.seek(0)
        out_file.truncate()
        out_file.writelines(all_lines)


def upload_to_steam():
    import json
    import subprocess

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
                                    ])

    print(upload_config.returncode)

    return upload_config.returncode


if __name__ == '__main__':
    builder_setup(appid, steam_sdk_dir, branch)
    depot_setup(appid, build_dir)
