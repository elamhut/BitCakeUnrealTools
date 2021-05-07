import unreal
import sys

blueprintName = "ARandomBlueprint"
blueprintPath = "/Game/Developers/nzxtdesktop"

createdAssetsCount = int(sys.argv[1])
createdAssetsName = str(sys.argv[2])
createdAssetsName += "%d"

factory = unreal.BlueprintFactory()

factory.set_editor_property("ParentClass", unreal.Character)

assetTools = unreal.AssetToolsHelpers.get_asset_tools()

for x in range(createdAssetsCount):
    myFile = assetTools.create_asset(createdAssetsName%(x), blueprintPath, None, factory)
    unreal.EditorAssetLibrary.save_loaded_asset(myFile)
