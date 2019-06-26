from fbs_runtime.application_context import ApplicationContext
from mainWidget import MainWindow
import qdarkgraystyle

import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    ui_base = appctxt.get_resource('ui_Cedar.ui')
    ui_settings = appctxt.get_resource('ui_Settings.ui')
    mainWin = MainWindow(ui_base,ui_settings)
    appctxt.app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    mainWin.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)