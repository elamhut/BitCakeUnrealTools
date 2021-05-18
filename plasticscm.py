import subprocess


def current_changeset():
    changeset_header = subprocess.Popen(['cm', 'status', '--head'], stdout=subprocess.PIPE)
    output, error = changeset_header.communicate()

    if error is None:
        output = output.decode('UTF-8')
        output = output.split("@")
        # Removing "cs:" from the string
        output = output[0][3:]
        return output

    else:
        return "Plastic SCM not Found"


if __name__ == '__main__':
    current_changeset()