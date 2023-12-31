# code in init_unreal.py wil run on startup if the plugin is enabled
import unreal
import unreal_qt
unreal_qt.setup()  


def create_script_editor_button():
    """Add a tool button to the tool bar"""

    section_name = 'Plugins'
    se_command = 'import unreal_batch_importer;unreal_batch_importer.show()'  
    label = 'alembic importer'
    tooltip = "An alembic batch importer plugin with houdini transform for unreal engine"

    menus = unreal.ToolMenus.get()
    level_menu_bar = menus.find_menu('LevelEditor.LevelEditorToolBar.PlayToolBar')
    level_menu_bar.add_section(section_name=section_name, label=section_name)

    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
    entry.set_label(label)
    entry.set_tool_tip(tooltip)
    entry.set_icon("EditorStyle","ContentBrowser.AssetActions.Edit")
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type=unreal.Name(''),  # not sure what this is
        string=se_command
    )
    level_menu_bar.add_menu_entry(section_name, entry)
    menus.refresh_all_widgets()
    print("menu created!")

## uncomment to add a button to the toolbar to launch your tool
## don't forget to modify the function
create_script_editor_button()


