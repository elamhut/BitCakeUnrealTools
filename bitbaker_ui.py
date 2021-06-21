import sys
import os
import unreal
import bitbaker_dataserializer as bds
import bitbaker_builder
import bitbaker_steamsdkmanager
from PySide6 import QtUiTools, QtWidgets

from importlib import *

reload(bds)
reload(bitbaker_builder)
reload(bitbaker_steamsdkmanager)

plugin_dir = unreal.Paths.project_plugins_dir()
plugin_dir = unreal.Paths.convert_relative_path_to_full(plugin_dir)
editor_level_lib = unreal.EditorLevelLibrary()
editor_asset_lib = unreal.EditorAssetLibrary()
asset_editor_sub = unreal.AssetEditorSubsystem()



class SimpleGUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SimpleGUI, self).__init__(parent)

        # load the created ui widget
        self.widget = QtUiTools.QUiLoader().load("{}BitBaker/Content/Python/UI/bitbaker.ui".format(plugin_dir))

        # attach the widget to the "self" GUI
        self.widget.setParent(self)

        # set the UI geometry (if UI is not centered/visible)
        self.widget.setGeometry(0, 0, self.widget.width(), self.widget.height())
        self.setFixedSize(770, 900)

        # get the data from the json so we can pre-fill fields with them
        baker_data = bds.load_bitbake_data()

        # find the interaction elements (XML structure)
        self.loginBox = self.widget.findChild(QtWidgets.QLineEdit, "loginBox")
        self.loginBox.setText(baker_data[0]['SteamLogin'])
        self.loginBox.editingFinished.connect(self.set_login)

        self.passwordBox = self.widget.findChild(QtWidgets.QLineEdit, "passwordBox")
        self.passwordBox.setText(baker_data[0]['SteamPassword'])
        self.passwordBox.editingFinished.connect(self.set_password)

        self.appidBox = self.widget.findChild(QtWidgets.QLineEdit, "appidBox")
        self.appidBox.setText(baker_data[0]['AppID'])
        self.appidBox.editingFinished.connect(self.set_appid)

        self.appbranchBox = self.widget.findChild(QtWidgets.QLineEdit, "appbranchBox")
        self.appbranchBox.setText(baker_data[0]['SteamBranch'])
        self.appbranchBox.editingFinished.connect(self.set_appbranch)

        self.steamsdkBox = self.widget.findChild(QtWidgets.QLineEdit, "steamsdkBox")
        self.steamsdkBox.setText(baker_data[0]['SteamSDKDirectory'])
        self.steamsdkBox.editingFinished.connect(self.steam_folderpath)

        self.buildfolderBox = self.widget.findChild(QtWidgets.QLineEdit, "buildfolderBox")
        self.buildfolderBox.setText(baker_data[0]['BuildDirectory'])
        self.buildfolderBox.editingFinished.connect(self.build_folderpath)

        # find buttons and set up handlers
        self.btn_stemsdk = self.widget.findChild(QtWidgets.QPushButton, "steamsdkFolderPicker")
        self.btn_stemsdk.clicked.connect(self.btn_steam_folderpath)

        self.btn_buildfolder = self.widget.findChild(QtWidgets.QPushButton, "buildFolderPicker")
        self.btn_buildfolder.clicked.connect(self.btn_build_folderpath)

        self.btn_buildandupload = self.widget.findChild(QtWidgets.QPushButton, "buildanduploadButton")
        self.btn_buildandupload.clicked.connect(self.build_and_upload)

        self.btn_buildonly = self.widget.findChild(QtWidgets.QPushButton, "buildonlyButton")
        self.btn_buildonly.clicked.connect(self.build_only)

        self.output_log = self.widget.findChild(QtWidgets.QListWidget, "outputLog")
        self.output_log.itemDoubleClicked.connect(self.open_asset)

        self.btn_testlog = self.widget.findChild(QtWidgets.QPushButton, "testOutputLog")
        self.btn_testlog.clicked.connect(self.setup_output)

    # Define functions for each field and button
    def set_login(self):
        value = self.loginBox.text()
        bds.data_serialize('SteamLogin', value)

    def set_password(self):
        value = self.passwordBox.text()
        bds.data_serialize('SteamPassword', value)

    def set_appid(self):
        value = self.appidBox.text()
        bds.data_serialize('AppID', value)

    def set_appbranch(self):
        value = self.appbranchBox.text()
        bds.data_serialize('SteamBranch', value)

    def steam_folderpath(self):
        value = self.steamsdkBox.text()
        if os.path.exists(value):
            bds.data_serialize('SteamSDKDirectory', value)
        else:
            QtWidgets.QMessageBox.warning(self, "Path Error!", "Path to SteamSDK does not exist!\nInvalid Path.")

    def build_folderpath(self):
        value = self.buildfolderBox.text()
        if os.path.exists(value):
            bds.data_serialize('BuildDirectory', value)
        else:
            QtWidgets.QMessageBox.warning(self, "Path Error!",
                                          "Path to the Build Folder does not exist!\nInvalid Path.")

    def btn_steam_folderpath(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        bds.data_serialize('SteamSDKDirectory', folderpath)
        self.steamsdkBox.setText(folderpath)

    def btn_build_folderpath(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        bds.data_serialize('BuildDirectory', folderpath)
        self.buildfolderBox.setText(folderpath)

    # Button functions that verify if all data is typed and correct
    def build_and_upload(self):
        verification = bds.data_verify()

        if len(verification) > 0:
            error_keys = []
            for entries in verification:
                error_keys.append(entries[0])

            QtWidgets.QMessageBox.warning(self, "Missing Data!",
                                          "{} Field(s) has(have) no data.".format(str(error_keys)[1:-2]))

        else:
            build = bitbaker_builder.build()
            bitbaker_steamsdkmanager.upload_to_steam(build)

    def setup_output(self):
        asset_editor = unreal.AssetEditorSubsystem()
        editor_asset = unreal.EditorAssetLibrary()

        with open("{}BitBaker/Content/Python/ConsoleLog.txt".format(plugin_dir), "r") as Log:
            broken_assets = []
            lines = Log.readlines()
            for line in lines:
                asset_paths = line.rstrip()
                asset_paths = asset_paths.split('|')
                self.output_log.addItem(str(asset_paths[0]))
                print(asset_paths)


    def open_asset(self, item):
        print(item.text())
        selected_asset = item.text()
        with open("{}BitBaker/Content/Python/ConsoleLog.txt".format(plugin_dir), "r") as Log:
            lines = Log.readlines()
            for line in lines:
                asset_paths = line.rstrip()
                asset_paths = asset_paths.split('|')
                if selected_asset == asset_paths[0]:
                    broken_assets = []
                    # Checks if there's a Map file extension in the errors, if so don't try to load it.
                    # Do this by splitting the '.' and getting the last string in the asset_paths
                    get_extension = asset_paths[0].split('.')
                    if get_extension[-1] != 'umap':
                        # Load the Asset then add it to the asset_paths so we can open it.
                        broken_assets.append(editor_asset_lib.load_asset(asset_paths[1]))
                        asset_editor_sub.open_editor_for_assets(broken_assets)
                    else:
                        editor_level_lib.load_level(asset_paths[1])



    def build_only(self):
        verification = bds.data_verify()

        if len(verification) > 0:
            for entries in verification:
                if entries[0] == 'BuildDirectory':
                    QtWidgets.QMessageBox.warning(self, "Missing Data!", "You need to set a Build Folder.")

        else:
            bitbaker_builder.build()

    def output_logger(self):
        with open("{}BitBaker/Content/Python/ConsoleLog.txt".format(plugin_dir), "r") as Log:
            for line in Log.readlines():
                self.output_log.addItem(str(line))


# Only create one instance of the GUI when it's not already running
app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)

if __name__ == '__main__':
    # Start the GUI
    main_window = SimpleGUI()
    main_window.show()
