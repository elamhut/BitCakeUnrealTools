import unreal
import subprocess
import os
import datetime
import json
import re
from bitbaker_steamsdkmanager import upload_to_steam

data_dir = os.path.dirname(__file__)
data_file = open("{}/generic_projectdata.json".format(data_dir), 'r')
bake_data = json.load(data_file)


# Get all the variables from the GUI
project_name = bake_data[0]['ProjectName']
appid = bake_data[0]['AppID']
steamsdk_user_dir = bake_data[0]['SteamSDKDirectory']
build_user_dir = bake_data[0]['BuildDirectory']

# Construct all necessary engine paths for the build
project_dir = unreal.Paths().project_dir()
project_dir = unreal.Paths().convert_relative_path_to_full(project_dir)
uproject_path = "{}{}.uproject".format(project_dir, project_name)
uproject_path = unreal.Paths().convert_relative_path_to_full(uproject_path)
engine_location = unreal.Paths().engine_dir()
engine_location = unreal.Paths().convert_relative_path_to_full(engine_location)
batch_files_dir = "{}Build/BatchFiles/".format(engine_location)


# editor_location = "{}Binaries/Win64/UE4Editor.exe".format(engine_location)
# editor_cmd_location = "{}Binaries/Win64/UE4Editor-cmd.exe".format(engine_location)


def build():
    build_config = subprocess.run(['{}RunUAT.bat'.format(batch_files_dir),
                                   '-ScriptsForProject="{}"'.format(uproject_path),
                                   'BuildCookRun',
                                   '-nocompileeditor',
                                   '-installed',
                                   '-nop4',
                                   '-project="{}"'.format(uproject_path),
                                   '-cook',
                                   '-stage',
                                   '-archive',
                                   '-archivedirectory="{}"'.format(build_user_dir),
                                   '-package',
                                   '-pak',
                                   '-prereqs',
                                   '-nodebuginfo',
                                   '-targetplatform=Win64',
                                   '-build_config',
                                   '-target=NekoNeko',
                                   '-clientconfig=Development',
                                   '-serverconfig=Development',
                                   '-utf8output'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

    # Decodes STDOUT so it can be manipulated correctly
    stdoutput = build_config.stdout.decode('UTF-8')

    if build_config.returncode == 0:
        print("Build Complete")
        return True
    else:
        treat_error(stdoutput)
        return False


def treat_error(stdoutput):
    # Open Console Log file so we can dump the treated errors inside
    with open("{}/ConsoleLog.txt".format(os.path.dirname(__file__)), "w+") as Log:
        splitted = stdoutput.split('\n')
        uniqueerrors = []
        for line in splitted:
            # Check if the line is an empty line \t\n\r only, no whitespaces
            if re.match(r'^\s*$', line):
                pass
            # Check for an error match according to Unreal's pattern and uniquely print it to the log
            else:
                matchgroup = re.search(r'.*Error: \[.*] (.*): \[.*:\s(.*)|.*ERROR: (.*)', line)
                if matchgroup is not None:
                    if matchgroup.group(1) is not None:
                        file_error = matchgroup.group(1) + '|' + matchgroup.group(2)
                    else:
                        file_error = matchgroup.group(3)

                    if file_error not in uniqueerrors:
                        uniqueerrors.append(file_error)
                        Log.write('Error: {}'.format(file_error))


def build_folder():
    # Construct Paths and Folder Name base on today's date
    date = datetime.datetime.now().strftime("%y%m%d")
    folder_name = "{}_{}".format(date, project_name)
    constructed_path = "{}/{}".format(build_user_dir, folder_name)

    # Check if there's already a build today and replace it, otherwise just rename the folder
    if os.path.isdir("{}".format(constructed_path)):
        from shutil import rmtree
        rmtree("{}".format(constructed_path))
        os.rename("{}/WindowsNoEditor/".format(build_user_dir), "{}".format(constructed_path))
    else:
        os.rename("{}/WindowsNoEditor/".format(build_user_dir), "{}".format(constructed_path))

    return folder_name


if __name__ == "__main__":
    # build()
    upload_to_steam()
