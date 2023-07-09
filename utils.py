import os
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
import cv2
import numpy as np
import time


def load_key():
    """Load the private key."""
    with open('C:\\Users\\mhhsu\\.android\\adbkey', 'r') as f:
        priv = f.read()
    signer = PythonRSASigner('', priv)
    return signer


def connect_device(signer, ip="127.0.0.1", port=62025):
    """Connect to the device."""
    device = AdbDeviceTcp(ip, port)
    device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
    return device


def take_screenshot(device):
    """Take a screenshot on the device and remove the saved screenshot."""
    device.shell('screencap -p /sdcard/screenshot.png')
    os.system('adb pull /sdcard/screenshot.png ./image/screenshot.png')
    device.shell('rm /sdcard/screenshot.png')
    time.sleep(0.1)


def swipe_screen(device, start_x, start_y, end_x, end_y, duration):
    """Swipe the device screen from one point to another."""
    device.shell(f'input swipe {start_x} {start_y} {end_x} {end_y} {duration}')


def match_template(main_image, template_path, threshold=0.8):
    """Match a template image on a main image and return the coordinates."""
    template = cv2.imread(template_path, 0)
    main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(main_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > threshold:
        center_x = max_loc[0] + (template.shape[1] / 2)
        center_y = max_loc[1] + (template.shape[0] / 2)
        return int(center_x), int(center_y)
    else:
        return None, None


def find_and_tap(device, template_path, threshold=0.8, delay=1):
    """Find a template in a screenshot and tap the screen."""
    while True:
        print('Finding template')
        take_screenshot(device)
        main_image = cv2.imread('image/screenshot.png')
        center_x, center_y = match_template(main_image, template_path, threshold)
        if center_x and center_y:
            device.shell(f'input tap {center_x} {center_y}')
            time.sleep(delay)
            return
        time.sleep(1)
def find(device, template_path, threshold=0.8):
    """Find a template in a screenshot and tap the screen."""
    take_screenshot(device)
    main_image = cv2.imread('image/screenshot.png')
    center_x, center_y = match_template(main_image, template_path, threshold)
    if center_x and center_y:
        return True
    else:
        return False

def tap(device, x, y, delay=0.5):
    device.shell(f'input tap {x} {y}')
    time.sleep(delay)

def tap_skill(device, chara, skill, choose=0, delay=0.5):
    x, y = 0, 600
    if chara == 1 and skill == 1:
        x = 50
    elif chara == 1 and skill == 2:
        x = 150
    elif chara == 1 and skill == 3:
        x = 250
    elif chara == 2 and skill == 1:
        x = 400
    elif chara == 2 and skill == 2:
        x = 450
    elif chara == 2 and skill == 3:
        x = 550
    elif chara == 3 and skill == 1:
        x = 700
    elif chara == 3 and skill == 2:
        x = 800
    elif chara == 3 and skill == 3:
        x = 900

    if choose == 0:
        device.shell(f'input tap {x} {y}')
        time.sleep(0.1)
        device.shell(f'input tap {x} {y}')
        time.sleep(1)
        return
    elif choose == 2:
        tap(device, x, y, delay)
        x = 640
        y = 360
    device.shell(f'input tap {x} {y}')
    time.sleep(0.1)
    device.shell(f'input tap {x} {y}')
    time.sleep(1)

def main():
    """Main function to control the device."""
    signer = load_key()
    device = connect_device(signer)
    take_screenshot(device)

    # Remaining logic for controlling the device

    print(device.shell("echo Hello World!"))


if __name__ == "__main__":
    main()
