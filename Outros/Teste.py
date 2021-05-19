import subprocess
import unreal

project_dir = unreal.Paths().project_dir()
changeset_header = subprocess.Popen(['cm', 'status', '--head'], cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = changeset_header.communicate()
print("Tem que printar aqui em baixo:")
print(output, error)