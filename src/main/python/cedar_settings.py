from PyQt5 import QtCore
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QVBoxLayout,QDialog,QFileDialog
from qt_organisation import Organisation

class cedarSettings:
    """
    The Dialog where settings are defined.

    Args:
        ui_settings(fbs resource): The file from which to build the ui.
    """


    def __init__(self,ui_settings,parent=None):
            super().__init__()


            self.cedarSettings=Organisation().use_namespace("CedarGeneral")

            self.ui =uic.loadUi(ui_settings)
            self.ui.resize(350, 200)

            self.ui.hostLineEdit.setText(self.cedarSettings.value("host","None"))
            self.ui.hostLineEdit.textChanged.connect(self.save_params)

            self.ui.userLineEdit.setText(self.cedarSettings.value("user","None"))
            self.ui.userLineEdit.textChanged.connect(self.save_params)

            self.ui.passwordLineEdit.setText(self.cedarSettings.value("password","None"))
            self.ui.passwordLineEdit.textChanged.connect(self.save_params)

            self.ui.databaseLineEdit.setText(self.cedarSettings.value("database","None"))
            self.ui.databaseLineEdit.textChanged.connect(self.save_params)

            self.ui.seedFileButton.clicked.connect(self.openFile)

            self.ui.fileSavelineEdit.setText(self.cedarSettings.value("seed_file"))


    def show(self):
        self.ui.show()

    def save_params(self):
        self.cedarSettings.setValue("host",self.ui.hostLineEdit.text())
        self.cedarSettings.setValue("user",self.ui.userLineEdit.text())
        self.cedarSettings.setValue("password",self.ui.passwordLineEdit.text())
        self.cedarSettings.setValue("database",self.ui.databaseLineEdit.text())


    def openFile(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname = QFileDialog.getSaveFileName(options=options)
        self.ui.fileSavelineEdit.setText(fname[0])
        self.cedarSettings.setValue("seed_file",self.ui.fileSavelineEdit.text())


