import unreal

menus = unreal.ToolMenus.get()

menus = menus.find_menu('LevelEditor.LevelEditorToolBar.CompileComboButton')
print(menus.menu_type)