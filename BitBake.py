import unreal
import subprocess
import os
import sys
import datetime
from shutil import rmtree


project_name = str(sys.argv[1])
appid = str(sys.argv[2])
steamsdk_user_dir = str(sys.argv[3])
build_user_dir = str(sys.argv[4])

project_dir = unreal.Paths().project_dir()
project_dir = unreal.Paths().convert_relative_path_to_full(project_dir)
uproject_path = "{}{}.uproject".format(project_dir, project_name)
uproject_path = unreal.Paths().convert_relative_path_to_full(uproject_path)

engine_location = unreal.Paths().engine_dir()
engine_location = unreal.Paths().convert_relative_path_to_full(engine_location)
editor_location = "{}Binaries/Win64/UE4Editor.exe".format(engine_location)
editor_cmd_location = "{}Binaries/Win64/UE4Editor-cmd.exe".format(engine_location)
batch_files_dir = "{}Build/BatchFiles/".format(engine_location)




def build():
    build = subprocess.run(['{}RunUAT.bat'.format(batch_files_dir),
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
                            '-build',
                            '-target=NekoNeko',
                            '-clientconfig=Development',
                            '-serverconfig=Development',
                            '-utf8output'])

    if build.returncode == 0:
        date = datetime.datetime.now().strftime("%y%m%d")
        folder_name = "{}_{}".format(date, project_name)
        constructed_path = "{}{}".format(build_user_dir, folder_name)
        if os.path.isdir("{}".format(constructed_path)):
            rmtree("{}".format(constructed_path))
            os.rename("{}WindowsNoEditor/".format(build_user_dir), "{}".format(constructed_path))
        else:
            os.rename("{}WindowsNoEditor/".format(build_user_dir), "{}".format(constructed_path))



if __name__ == "__main__":
    # build()
    print(project_name)
    print(appid)
    print(steamsdk_user_dir)
    print(build_user_dir)