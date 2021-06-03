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


ui_dir = unreal.Paths.project_plugins_dir()
ui_dir = unreal.Paths.convert_relative_path_to_full(ui_dir)
editor_level_lib = unreal.EditorLevelLibrary()


class SimpleGUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SimpleGUI, self).__init__(parent)

        # load the created ui widget
        self.widget = QtUiTools.QUiLoader().load("{}BitBaker/Content/Python/UI/bitbaker.ui".format(ui_dir))

        # attach the widget to the "self" GUI
        self.widget.setParent(self)

        # set the UI geometry (if UI is not centered/visible)
        self.widget.setGeometry(0, 0, self.widget.width(), self.widget.height())
        self.setFixedSize(770, 850)

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
            QtWidgets.QMessageBox.warning(self, "Path Error!", "Path does not exist!\nInvalid Path.")

    def build_folderpath(self):
        value = self.buildfolderBox.text()
        if os.path.exists(value):
            bds.data_serialize('BuildDirectory', value)
        else:
            QtWidgets.QMessageBox.warning(self, "Path Error!", "Path does not exist!\nInvalid Path.")

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

            QtWidgets.QMessageBox.warning(self, "Missing Data!", "{} Field(s) has(have) no data.".format(str(error_keys)[1:-2]))

        else:
            build = bitbaker_builder.build()
            bitbaker_steamsdkmanager.upload_to_steam(build)

    def build_only(self):
        verification = bds.data_verify()

        if len(verification) > 0:
            for entries in verification:
                if entries[0] == 'BuildDirectory':
                    QtWidgets.QMessageBox.warning(self, "Missing Data!", "You need to set a Build Folder.")

        else:
            bitbaker_builder.build()



# Only create one instance of the GUI when it's not already running
app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)

if __name__ == '__main__':
    # Start the GUI
    main_window = SimpleGUI()
    main_window.show()
