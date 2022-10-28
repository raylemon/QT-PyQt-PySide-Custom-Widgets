# IMPORT GUI FILE
from ui_interface import *
# IMPORT Custom widgets
from Custom_Widgets.Widgets import *

# INITIALIZE APP SETTINGS
settings = QSettings()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # APPLY JSON STYLESHEET

        loadJsonStyle(self, self.ui)

        self.show()



if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

