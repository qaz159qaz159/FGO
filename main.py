import time
from scripts import *
from utils import DeviceController

def main():
    """Main function to control the device."""
    device_controller = DeviceController()
    fgo_script = FGOscript(device_controller)
    fgo_script.week(rounds=1, task=0)

def screenshot():
    """Take screenshot."""
    device_controller = DeviceController()
    device_controller.screenshot()

if __name__ == '__main__':
    main()
    # screenshot()