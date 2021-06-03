import unreal

editor_level_lib = unreal.EditorLevelLibrary()
editor_filter_lib = unreal.EditorFilterLibrary()

level_actors = editor_level_lib.get_all_level_actors()
static_mesh_actors = editor_filter_lib.by_class(level_actors, unreal.StaticMeshActor)
deleted = 0

for actor in static_mesh_actors:
    actor_name = actor.get_fname()

    actor_mesh_comp = actor.static_mesh_component
    actor_mesh = actor_mesh_comp.static_mesh

    is_valid_actor = actor_mesh != None

    if not is_valid_actor:
        actor.destroy_actor()
        deleted += 1
        unreal.log("The Mesh Component of Actor {} was Null and so it was deleted".format(actor_name))

    unreal.log("{} actor has mesh {}".format(actor_name, actor_mesh))

unreal.log("Deleted {} Actors with Invalid Meshes".format(deleted))