import unreal

blueprintName = "ARandomBlueprint"
blueprintPath = "/Game/Developers/nzxtdesktop"

factory = unreal.BlueprintFactory()

factory.set_editor_property("ParentClass", unreal.GameMode)

assetTools = unreal.AssetToolsHelpers.get_asset_tools()
myFile = assetTools.create_asset(blueprintName, blueprintPath, None, factory)

unreal.EditorAssetLibrary.save_loaded_asset(myFile)
