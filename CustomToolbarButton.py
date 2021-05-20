import unreal
import os


menus = unreal.ToolMenus.get()

menu_name = "LevelEditor.LevelEditorToolBar"
menu = menus.find_menu(menu_name)

# NOTE 生成类型改为 Toolbar 的按钮
entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
entry.set_label("BitCake Tools")
# NOTE 注册执行的命令
typ = unreal.ToolMenuStringCommandType.PYTHON
with open('{}/RunEditorUtilityWidget.py'.format(os.path.dirname(__file__)), 'r') as runwidget:
    pythoncode = runwidget.read()

entry.set_string_command(typ, "", pythoncode)
menu.add_menu_entry('File', entry)

# NOTE 添加刷新才能立刻看到添加的效果
menus.refresh_all_widgets()