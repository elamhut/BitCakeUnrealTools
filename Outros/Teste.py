import unreal


def list_menu(num=1000):
    menu_list = set()
    for i in range(num):
        obj = unreal.find_object(None, "/Engine/Transient.ToolMenus_0:ToolMenu_%s" % i)
        if not obj:
            continue
        menu_name = str(obj.menu_name)
        if menu_name != "None":
            menu_list.add(menu_name)
    return list(menu_list)


print(list_menu())
LogPython: ['LevelEditor.LevelEditorToolBar', 'ContentBrowser.AssetContextMenu.LevelSequence',
            'MediaPlayer.AssetPickerAssetContextMenu', 'ContentBrowser.AssetContextMenu',
            'LevelEditor.LevelEditorToolBar.CompileComboButton', 'MainFrame.MainMenu', 'LevelEditor.MainMenu.Edit',
            'LevelEditor.LevelEditorToolBar.BuildComboButton.LightingInfo.LightingResolution', 'LevelEditor.MainMenu',
            'LevelEditor.MainMenu.File', 'AssetEditor.SkeletalMeshEditor.ToolBar', 'MainFrame.MainMenu.Edit',
            'ContentBrowser.AssetContextMenu.CameraAnim', 'LevelEditor.MainMenu.Window',
            'LevelEditor.LevelEditorToolBar.BuildComboButton',
            'LevelEditor.LevelEditorToolBar.BuildComboButton.LightingQuality', 'MainFrame.MainMenu.File',
            'LevelEditor.LevelEditorToolBar.BuildComboButton.LightingInfo.LightingDensity',
            'LevelEditor.ActorContextMenu', 'ContentBrowser.AssetContextMenu.SoundWave', 'MainFrame.MainTabMenu.File',
            'LevelEditor.LevelEditorToolBar.SourceControl',
            'LevelEditor.LevelEditorToolBar.BuildComboButton.LightingInfo',
            'LevelEditor.LevelEditorSceneOutliner.ContextMenu', 'MainFrame.MainMenu.Window',
            'LevelEditor.LevelEditorToolBar.LevelToolbarQuickSettings', 'MainFrame.MainMenu.Asset',
            'LevelEditor.LevelEditorToolBar.Cinematics', 'LevelEditor.MainMenu.Help',
            'LevelEditor.LevelEditorToolBar.EditorModes', 'MainFrame.MainMenu.Help', 'ContentBrowser.FolderContextMenu',
            'LevelEditor.LevelEditorToolBar.OpenBlueprint']
