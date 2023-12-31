
# ######################################
# an alembic batch importer plugin with houdini transform for unreal engine 

# Be sure to add your default python modules directory path to Unreal:
# Project Settings -> Python -> Additional Paths
# "Your-Unreal-project-path\\Content\\Python\\Lib\\site-packages"

# This code required PySide2 module which may need to be installed.
# To install required modules open windows command prompt and enter:
# pip install --target="Your-Unreal-project-path\Content\Python\Lib\site-packages" --no-user pyside2
# pip install --target="Your-Unreal-project-path\Content\Python\Lib\site-packages" --no-user unreal-qt
# python -m pip install --target="Your-Unreal-project-path\Content\Python\Lib\site-packages" --no-user unreal-stylesheet
# ######################################

import unreal
from PySide2 import QtWidgets, QtCore, QtGui, QtUiTools
from PySide2.QtWidgets import QApplication, QLabel, QDialog, QWidget, QProgressBar, QPushButton
from pathlib import Path
import os


class ImporterWidget(QWidget):
    def __init__(self, *args):
        super(ImporterWidget, self).__init__(*args)

        self.setWindowTitle("Alembic Batch Importer")

        button1 = QPushButton("Select Files")
        button1.clicked.connect(self.choose_dir_button_clicked)

        button2 = QPushButton("Import All Alembics")
        button2.clicked.connect(self.batchImport)

        label = QLabel("Import Destination: ")
        self.inPath = QtWidgets.QLineEdit()
        self.inPath.setPlaceholderText("example: /Game/ABC")
        self.inPath.textChanged.connect(self.chooseSavePath)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(label)
        h_layout.addWidget(self.inPath)

        ifHoudiniBox = QtWidgets.QCheckBox("Transform from Houdini Space?")
        ifHoudiniBox.setChecked(True)
        ifHoudiniBox.toggled.connect(self.houdini_box_toggled)

        button_layout = QtWidgets.QVBoxLayout(self)
        button_layout.addLayout(h_layout)
        button_layout.addWidget(ifHoudiniBox)
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)

        self.setLayout(button_layout)


        # # connect tab change
        # self.tab_widget.currentChanged.connect(self.search_current_tab)

     
        # self.ABC_SOURCE_DIR = Path("D:\\Efiles\\Unreal Projects\\20231206_FX_test\\HDARender")
        self.ABC_SOURCE_DIR = ""
        self.VALID_EXTS = (".abc")
        self.DEST_DIR_UE = ""
        self.SAVE_FREQ = 5 # save every 5 assets imported
        self.asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        self.ifHoudiniSpace = True

    def houdini_box_toggled(self,checked):
        if(checked):
            self.ifHoudiniSpace = True
        else:
            self.ifHoudiniSpace = False

    def choose_dir_button_clicked(self):
        dir_name= QtWidgets.QFileDialog.getExistingDirectory(self, "Choose Folder")
        if((dir_name == "")):
            return
        print("file :",dir_name)
        self.ABC_SOURCE_DIR = Path(dir_name)

    def chooseSavePath(self, text=None):
        if text is None:
            text = self.inPath.text()
        self.DEST_DIR_UE = text
    
    def saveAll():
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages(
                        save_map_packages=False, save_content_packages=True
                    )

    def batchImport(self):
        if self.DEST_DIR_UE == "":
            QtWidgets.QMessageBox.information(self,"Message","Please enter a valid save path first!")

            
        if os.path.isdir(self.ABC_SOURCE_DIR) != True:
            QtWidgets.QMessageBox.information(self,"Message","Please select a valid folder first!")


        # Set the import settings for Alembic
        alembic_settings = unreal.AbcImportSettings()


        path_to_import = list()
        for file_path_abs in self.ABC_SOURCE_DIR.iterdir():
            if file_path_abs.suffix not in self.VALID_EXTS:
                    continue
            path_to_import.append(file_path_abs)
        
        if len(path_to_import) == 0:
            QtWidgets.QMessageBox.information(self,"Message","No alembic file was found in selected directory!")
            pass

        else:
            num_assets_to_save= 0
            with unreal.ScopedSlowTask(len(path_to_import), "Batch importing Alembic files") as slow_task:
                slow_task.make_dialog(True) 
                n = 1
                for file_path_abs in path_to_import:
                    if slow_task.should_cancel():
                        break
                    slow_task.enter_progress_frame(1, "Batch importing Alembic files  " + str(n) + ' / ' + str(len(path_to_import)))

                    if file_path_abs.suffix not in self.VALID_EXTS:
                        continue
                    name = file_path_abs.stem
                    file_name_parts = name.split("_")
                    file_name_start = file_name_parts[0]
                    only_letters = [ch for ch in file_name_start if ch.isalpha()]
                    tex_category = "".join(only_letters)


                    task = unreal.AssetImportTask()
                    task.filename =  str(file_path_abs)
                    task.destination_path = self.DEST_DIR_UE
                    task.automated = True
                    task.replace_existing = True
                    task.async_ = True
                    task.save = False

                    if self.ifHoudiniSpace is True:
                        # Assign the Alembic settings to the import task
                          # Customize Alembic import settings here if needed
                        alembic_settings.conversion_settings = unreal.AbcConversionSettings(
                        scale=unreal.Vector(100, -100, 100),  # Set the scale using a Vector (adjust the values accordingly)
                        rotation=unreal.Vector(90, 0.0, 0.0)  # Set the rotation using a Vector (adjust the values accordingly)
                        )
                    
                    alembic_settings.import_type = unreal.AlembicImportType.GEOMETRY_CACHE
                    task.options = alembic_settings


                    # Execute the import task
                    self.asset_tools.import_asset_tasks([task])

                    n += 1
                    num_assets_to_save += 1
                    if num_assets_to_save >= self.SAVE_FREQ:
                        unreal.EditorLoadingAndSavingUtils.save_dirty_packages(
                            save_map_packages=False, save_content_packages=True
                        )
                        num_assets_to_save = 0

      



def show():
    global window
    window = ImporterWidget()
    window.resize(500, 250)
    window.show()

    # app = QApplication([])
    import unreal
    unreal.parent_external_window_to_slate(window.winId())
    # app.exec_()


show()    
