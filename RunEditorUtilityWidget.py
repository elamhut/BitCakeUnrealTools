import unreal

bitbaker = unreal.EditorAssetLibrary.load_asset("/BitBaker/BitBaker.BitBaker")
unreal.EditorUtilitySubsystem().spawn_and_register_tab(bitbaker)
