import unreal

editor_asset_lib = unreal.EditorAssetLibrary()
string_lig = unreal.StringLibrary()

source_dir = "/Game/"
include_subfolders = True
set_texture = 0

assets = editor_asset_lib.list_assets(source_dir, recursive=include_subfolders)
color_patterns = ["_ORM", "_OcclusionRoughnessMetallic", "_Metallic", "_Roughness", "_Mask"]

for asset in assets:
    for pattern in color_patterns:
        if string_lig.contains(asset, pattern):
            # load the asset, turn off sRGB and set compression to TC_Mask
            asset_obj = editor_asset_lib.load_asset()
            asset_obj.set_editor_property("sRGB", False)
            asset_obj.set_editor_property("CompressionSettings", unreal.TextureCompressionSettings.TC_MASKS)


            unreal.log("Setting TC_Masks and turning off sRGB for asset {}".format(asset))
            set_texture += 1
            break


    unreal.log("Linear color for matching texture set for {} assets".format(set_texture))