# Unreal Alembic Batch Importer Plugin
An alembic batch importer plugin in Unreal Engine 5.2 with Houdini space transform option. <br>
Using this plugin you can easily import multiple alembic simulations as geocache from Houdini without checking settings everytime.


![alembicbatchimporter](https://github.com/wzhang1998/unreal-alembic-batch-importer/assets/67906283/ed2cc24b-eb44-4425-867d-593eb66870de)
<img src="https://github.com/wzhang1998/unreal-alembic-batch-importer/assets/67906283/5bcb662f-4b6a-49b1-bd20-6e0625fa4ae2" width='691'><br>

## Install 
- Install required packages:
    - option 1：pip install the Python dependencies to `...\Your-Unreal-Project\Content\Python\Lib\site-packages` (you can use `--target` with pip install)
        - PySide2
        - unreal-qt
    - option 2 (recommended)：Copy the pre-download library (`Python` folder) to your Unreal project's `Content` folder `...\Your-Unreal-Project\Content\Python`
- Copy the folder to your Unreal project's plugin folder `...\Your-Unreal-Project\Plugins\alembicBatchImporter`
- Restart Unreal and Enable the plugin

## Prerequisites
- In Unreal Editor, open `Edit - Plugins` window, enable `Alembic Importer` plugin
    ![alembicimporter](https://github.com/wzhang1998/unreal-alembic-batch-importer/assets/67906283/92a92d42-4cf5-4613-9838-74c263707d02)
- Add `...\Your-Unreal-Project\Content\Python\Lib\site-packages` to your editor python path, see [Unreal doc](https://docs.unrealengine.com/5.2/en-US/scripting-the-unreal-editor-using-python/#pythonpathsintheunrealeditor)

## How to use?
- When the plugin enabled, a button will add to editor tool bar, press the button, and a window like this will show up.
<img src="https://github.com/wzhang1998/unreal-alembic-batch-importer/assets/67906283/a7459d59-9773-4916-9141-62187a03cbf9" ><br>
<img src="https://github.com/wzhang1998/unreal-alembic-batch-importer/assets/67906283/2c73e61a-43e8-4aaa-af25-77b843a50969" width='518'><br>
- `Import Destination`: Type in your alembic geocache import destination, eg: `/Game/ABC`.
- `Transform from Houdini Space?`: Choose your import transform space, by default it sets to from Houdini space to Unreal space: scale=unreal.Vector(100, -100, 100), rotation=unreal.Vector(90, 0.0, 0.0).
- `Select Files`: Choose your .abc file folder from the computer.
- `Import All Alembics`: Import all at once!!

## Tips
- I used this script to change all geocaches' material
```python
    def returnMaterialInformationSMC():

    levelActors = unreal.EditorActorSubsystem().get_all_level_actors()
    testMat = unreal.EditorAssetLibrary.find_asset_data('/Game/StarterContent/Materials/M_AssetPlatform.M_AssetPlatform').get_asset() # replace your material path

    for levelActor in levelActors:
        if (levelActor.get_class().get_name()) == 'GeometryCacheActor':
            geometryCacheComponent = levelActor.geometry_cache_component

            print(levelActor.get_name())
            materials = geometryCacheComponent.get_materials()
            for material in materials:
                print(material.get_name())
                try:
                    for item in material.texture_parameter_values: print(item)
                except:
                    pass
                print('_')

            for i in range(geometryCacheComponent.get_num_materials()):
                geometryCacheComponent.set_material(i, testMat)

    returnMaterialInformationSMC()
```



