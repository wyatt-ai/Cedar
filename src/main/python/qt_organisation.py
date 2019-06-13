from PyQt5.QtCore import QSettings

class Organisation(QSettings):
  
    def __init__(self):
        super().__init__()

    def use_namespace(self,namespace):

      #organization,application
      self.settings = QSettings("WyattAI", namespace)

      return self.settings