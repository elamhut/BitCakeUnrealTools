import os
import unreal

editor_utility = unreal.EditorUtilityLibrary()
asset_editor = unreal.AssetEditorSubsystem()
editor_asset = unreal.EditorAssetLibrary()
asset_registry_helper = unreal.AssetRegistryHelpers()
gameplay_statics = unreal.GameplayStatics()
editor_level = unreal.EditorLevelLibrary()

def open_asset():
    assets = []
    selected_assets = editor_utility.get_selected_assets()

    for asset in selected_assets:
        assets.append(asset)

    asset_editor.open_editor_for_assets(assets)

def setup_output():
    with open("D:/NekoNeko/Plugins/BitBaker/Content/Python/ConsoleLog.txt".format(os.path.dirname(__file__)), "r") as Log:
        broken_assets = []
        lines = Log.readlines()
        for line in lines:
            asset_paths = line.rstrip()
            asset_paths = asset_paths.split('|')
            print(asset_paths)
            # Checks if there's a Map file extension in the errors, if so don't try to load it.
            # Do this by splitting the '.' and getting the last string in the asset_paths
            get_extension = asset_paths[0].split('.')
            if get_extension[-1] != 'umap':
                # Load the Asset then add it to the asset_paths so we can open it.
                broken_assets.append(editor_asset.load_asset(asset_paths[1]))
                asset_editor.open_editor_for_assets(broken_assets)

            # else:
            #     broken_assets.append(load)

        print(broken_assets)


def load_level(path):
    editor_level.load_level(path)


if __name__ == '__main__':
    # load_level(r'D:\NekoNeko\Content\NekoNeko\Core\GameModes\BP_Main_GameStateBase.uasset')
    setup_output()
