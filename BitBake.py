import unreal
import subprocess


project_name = "NekoNeko"
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
    build= subprocess.run(['{}RunUAT.bat'.format(batch_files_dir),
                     '-ScriptsForProject="{}"'.format(uproject_path),
                     'BuildCookRun',
                     '-nocompileeditor',
                     '-installed',
                     '-nop4',
                     '-project="{}"'.format(uproject_path),
                     '-cook',
                     '-stage',
                     '-archivedirectory="{}Build"'.format(project_dir),
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

    print(build)
    print("Return Code:")
    print(build.returncode)


if __name__ == "__main__":
    build()
