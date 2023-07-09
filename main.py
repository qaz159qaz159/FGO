import time
from scripts import *
from utils import DeviceController
from app import Application
from PySide6.QtWidgets import QApplication
import sys


def screenshot():
    """Take screenshot."""
    device_controller = DeviceController()
    device_controller.screenshot()


def main():
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create an Application instance
    application = Application(app)

    # Run the application
    application.run()


if __name__ == '__main__':
    main()
    # screenshot()
