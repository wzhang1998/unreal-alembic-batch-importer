# Unreal Alembic Batch Importer Plugin
An alembic batch importer plugin in Unreal Engine 5.2 with Houdini space transform option. <br>
Using this plugin you can easily import multiple alembic simulations as geocache from Houdini without checking settings everytime.

### Install 
- Install required packages:
    - option 1：pip install the Python dependencies to `...\Your-Unreal-Project\Content\Python\Lib\site-packages` (you can use `--target` with pip install)
        - PySide2
        - unreal-qt
    - option 2 (recommended)：Copy the pre-download library (`Python` folder) to your Unreal project's `Content` folder `...\Your-Unreal-Project\Content\Python`
- Copy the folder to your Unreal project's plugin folder `...\Your-Unreal-Project\Plugins\alembicBatchImporter`
- Restart Unreal and Enable the plugin

### Prerequisites
- In Unreal Editor, open `Edit - Plugins` window, enable `Alembic Importer` plugin
- Add `...\Your-Unreal-Project\Content\Python\Lib\site-packages` to your editor python path, see [Unreal doc](https://docs.unrealengine.com/5.2/en-US/scripting-the-unreal-editor-using-python/#pythonpathsintheunrealeditor)

### How to use?

