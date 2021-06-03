import unreal
import os


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