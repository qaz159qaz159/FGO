import sys
from scripts import *
from utils import DeviceController
from window import MainWindow


class Application:
    def __init__(self, app):
        self.device_controller = DeviceController()
        self.main_window = MainWindow()
        self.fgo_script = FGOscript(self.device_controller, self.main_window)
        self.main_window.set_fgo_script(self.fgo_script)
        self.app = app

    def run(self):
        # Show the main window
        self.main_window.show()
        # Start the Qt event loop
        sys.exit(self.app.exec())
