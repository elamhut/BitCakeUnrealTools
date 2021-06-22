import subprocess
import unreal
from datetime import datetime


def check_for_vcs():
    # Check if there's a .plastic folder and if so,
    project_dir = unreal.Paths().project_dir()
    project_dir = unreal.Paths().convert_relative_path_to_full(project_dir)
    plastic_dir = "{}.plastic".format(project_dir)

    if unreal.Paths.directory_exists(plastic_dir):
        return current_changeset()
    else:
        now = datetime.now()
        date_string = now.strftime("%d/%m/%Y %H:%M:%S")
        return date_string

def current_changeset():

    project_dir = unreal.Paths().project_dir()
    project_dir = unreal.Paths().convert_relative_path_to_full(project_dir)

    changeset_header = subprocess.Popen(['cm', 'status', '--head'],
                                        cwd=project_dir,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE
                                        )
    output, error = changeset_header.communicate()

    if error.decode('UTF-8') == '':
        output = output.decode('UTF-8')
        output = output.split("@")
        # Removing "cs:" from the string
        output = output[0][3:]
        return output


if __name__ == '__main__':
    print(check_for_vcs())