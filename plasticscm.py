import subprocess
import unreal



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

    else:
        return "Plastic SCM not Found"


if __name__ == '__main__':
    print(current_changeset())