import subprocess
import unreal
import os

try:
    import vdf
except ImportError:
    engine_location = unreal.Paths().engine_dir()
    engine_location = unreal.Paths().convert_relative_path_to_full(engine_location)
    python_location = engine_location + r"\Binaries\ThirdParty\Python3\Win64\python.exe"

    plugin_location = unreal.Paths().project_plugins_dir()
    plugin_location = unreal.Paths().convert_relative_path_to_full(plugin_location)
    requirements_location = plugin_location + r"\BitBaker\Content\Python\requirements.txt"

    print("Engine Location" + python_location)
    print("Starting Pip Install")
    tryinstall = subprocess.run([python_location, "-m", "pip", "install", "-r", requirements_location, "--user"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stderror = tryinstall.stderr.decode('UTF-8')
    print(stderror)
    print("*" * 40)
    print("Finished Pip Install")


menus = unreal.ToolMenus.get()

menu_name = "LevelEditor.LevelEditorToolBar"
menu = menus.find_menu(menu_name)

entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
entry.set_label("BitCake Tools")

typ = unreal.ToolMenuStringCommandType.PYTHON
with open('{}/bitbaker_ui.py'.format(os.path.dirname(__file__)), 'r') as runwidget:
    pythoncode = runwidget.read()

entry.set_string_command(typ, "", pythoncode)
menu.add_menu_entry('File', entry)

menus.refresh_all_widgets()