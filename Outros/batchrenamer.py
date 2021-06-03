import unreal
import sys

from PySide6 import QtCore, QtGui, QtUiTools, QtWidgets


def rename_assets(search_pattern, replace_pattern, use_case):
    # instances of unreal classes
    system_lib = unreal.SystemLibrary()
    editor_util = unreal.EditorUtilityLibrary()
    string_lib = unreal.StringLibrary()

    # get the selected assets
    selected_assets = editor_util.get_selected_assets()
    num_assets = len(selected_assets)
    replaced = 0

    unreal.log("Selected {} assets".format(num_assets))

    # loop over each asset and rename
    for asset in selected_assets:
        asset_name = system_lib.get_object_name(asset)
        print(asset_name)

        contains = string_lib.contains(asset_name, search_pattern, use_case=False)
        print("Does the asset name {} contains the string {} inside it? A: {}".format(asset_name, search_pattern, contains))

        # check if the asset name contains the given string to be replaced
        if string_lib.contains(asset_name, search_pattern, use_case=use_case):
            search_case = unreal.SearchCase.CASE_SENSITIVE if use_case else unreal.SearchCase.IGNORE_CASE
            replaced_name = string_lib.replace(asset_name, search_pattern, replace_pattern, search_case=search_case)
            editor_util.rename_asset(asset, replaced_name)

            replaced += 1
            unreal.log("Replaced {} with {}".format(asset_name, replaced_name))

        else:
            unreal.log("{} did not match the search pattern, was skipped".format(asset_name))

    unreal.log("Replaced {} of {} assets".format(replaced, num_assets))

class RenameGUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RenameGUI, self).__init__(parent)
        self.setFixedSize(350, 180)

        # load the created GUI
        self.widget = QtUiTools.QUiLoader().load(r"D:\NekoNeko\Plugins\BitBaker\Content\Python\UI\renamer.ui")
        self.widget.setParent(self)

        self.widget.setGeometry(0, 0, self.widget.width(), self.widget.height())

        # find the interaction element
        self.search = self.widget.findChild(QtWidgets.QLineEdit, "textToReplace")
        self.replace = self.widget.findChild(QtWidgets.QLineEdit, "newTextHere")

        self.use_case = self.widget.findChild(QtWidgets.QCheckBox, "caseSensitive")

        # find and assing the trigger to pushbutten
        self.rename_button = self.widget.findChild(QtWidgets.QPushButton, "rename")
        self.rename_button.clicked.connect(self.rename_handler)

    def rename_handler(self):
        search_pattern = self.search.text()
        replace_pattern = self.replace.text()
        use_case = self.use_case.isChecked()

        rename_assets(search_pattern, replace_pattern, use_case)

app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)

window = RenameGUI()
window.show()