import sys
from PySide6 import QtCore, QtGui, QtUiTools, QtWidgets

class Example(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setup()

    def setup(self):
        button_quit = QtWidgets.QPushButton('Force Quit', self)
        button_quit.clicked.connect(QtWidgets.QApplication.instance().quit)
        button_quit.resize(button_quit.sizeHint())
        button_quit.move(90, 100)

        self.setGeometry(100, 100, 200, 150)
        self.setWindowTitle('Window Example')

        self.show()

    def closeEvent(self, event:QtGui.QCloseEvent):
        reply = QtWidgets.QMessageBox.question(self, 'Message', 'Are you sure you want to quit, bitch?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def run():
    app = QtWidgets.QApplication([])

    ex = Example()

    app.exec_()

if __name__ == '__main__':
    run()


# class SimpleGUI(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super(SimpleGUI, self).__init__(parent)
#
#         # load the created ui widget
#         self.widget = QtUiTools.QUiLoader().load("D:\\NekoNeko\\Plugins\\BitBaker\\Content\\Python\\UI\\bitbaker.ui")
#
#         # attach the widget to the "self"GUI
#         self.widget.setParent(self)
#
#
# app = None
# if not QtWidgets.QApplication.instance():
#     app = QtWidgets.QApplication(sys.argv)
#
# if __name__ == '__main__':
#     # Start the GUI
#     main_window = SimpleGUI()
#     main_window.show()
