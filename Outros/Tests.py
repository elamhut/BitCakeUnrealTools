import unreal

editor_utility = unreal.EditorUtilityLibrary()
asset_editor = unreal.AssetEditorSubsystem()
editor_asset = unreal.EditorAssetLibrary()
gameplay_statics = unreal.GameplayStatics()
editor_level = unreal.EditorLevelLibrary()

def open_asset():
    assets = []
    selected_assets = editor_utility.get_selected_assets()

    for asset in selected_assets:
        assets.append(asset)

    asset_editor.open_editor_for_assets(assets)

def find_asset(path):
    does_asset_exist = editor_asset.find_asset_data(path)
    print(does_asset_exist)
    empty = []
    empty.append(does_asset_exist.get_asset())
    print(empty)
    asset_editor.open_editor_for_assets(empty)
    # print(does_asset_exist)

def load_level(path):
    editor_level.load_level(path)


if __name__ == '__main__':
    load_level('/Game/NekoNeko/Maps/Sandbox/Sandbox_P.umap')
# find_asset('/Game/NekoNeko/Maps/Sandbox/Sandbox_P.umap')