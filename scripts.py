import time
import cv2
import numpy as np
from PySide6.QtCore import Signal, QObject
class FGOscript:
    def __init__(self, device_controller, main_window):
        self.dc = device_controller
        self.match_counter = 0
        self.main_window = main_window

    def week(self, rounds=1, task=0, team=1):
        """
        :param rounds:
        :param task: 0 for QP, 1 for EXP
        :param team: 0 for blue, 1 for red
        :return:
        """
        pics = []
        if task == 0 and team == 0:
            pics = ['image/c_caster_qp1.png', 'image/c_caster_qp2.png', 'image/c_caster_qp3.png']
        elif task == 1 and team == 0:
            pics = ['image/c_caster_exp1.png', 'image/c_caster_exp2.png', 'image/c_caster_exp3.png',
                    'image/c_caster_exp4.png']
        elif task == 1 and team == 1:
            pics = ['image/fox_assassin_exp1.png', 'image/fox_assassin_exp2.png']

        self.dc.take_screenshot()
        if team == 0:
            self.blue(pics, rounds)
        elif team == 1:
            self.red(pics, rounds)

    def blue(self, pics, rounds=1):
        for i in range(rounds):
            print(f'Round {i + 1}')
            self.dc.find_and_tap('image/wizard.png')
            print('Find caster.')

            while not any(self.dc.find(pic) for pic in pics):
                print('Waiting for friend list.')
                self.dc.swipe_screen(800, 600, 800, 400, 500)
                if self.dc.find('image/friend_end_list.png', threshold=0.92):
                    print('Friend list end.')
                    self.dc.find_and_tap('image/new_friends.png')
                    print('Find new friends.')
                    self.dc.find_and_tap('image/new_friends_check.png')
                    print('Find new friends check.')
            found_pic = next(pic for pic in pics if self.dc.find(pic))
            self.dc.find_and_tap(found_pic)
            print('Find blue money chara.')
            if i == 0:
                # time.sleep(3)
                # self.dc.tap(520, 40, delay=1)
                # self.dc.tap(1000, 650, delay=1)
                self.dc.find_and_tap('image/battle_start.png', threshold=0.7)
                print('Find battle start.')
            while not self.dc.find('image/attack.png', threshold=0.7):
                time.sleep(1)
                pass

            self.dc.tap_skill(1, 1, choose=0, delay=1)
            self.dc.tap_skill(1, 2, choose=2, delay=1)
            self.dc.tap_skill(1, 3, choose=2, delay=1)
            self.dc.tap_skill(2, 1, choose=0, delay=1)
            self.dc.tap_skill(2, 2, choose=0, delay=1)
            self.dc.tap_skill(2, 3, choose=0, delay=1)
            self.dc.tap_skill(3, 1, choose=0, delay=1)
            self.dc.tap_skill(3, 2, choose=2, delay=1)
            self.dc.tap_skill(3, 3, choose=2, delay=1)
            self.dc.find_and_tap('image/attack.png')
            print('Find attack.')
            self.dc.tap(640, 300)
            self.dc.tap(640, 500)
            self.dc.tap(850, 500)
            self.dc.take_screenshot()
            self.dc.find_and_tap('image/attack.png')
            print('Find attack.')
            self.dc.tap(640, 300)
            self.dc.tap(640, 500)
            self.dc.tap(850, 500)
            self.dc.take_screenshot()
            self.dc.find_and_tap('image/people_skill.png')
            print('Find people skill.')
            self.dc.tap(900, 300)
            self.dc.find_and_tap('image/attack.png')
            print('Find attack.')
            self.dc.tap(640, 300)
            self.dc.tap(640, 500)
            self.dc.tap(850, 500)
            self.dc.find_and_tap('image/end_battle.png')
            print('Find end battle.')
            self.dc.find_and_tap('image/end_battle_2.png')
            print('Find end battle 2.')
            self.main_window.count_and_add('image/material/cristal.png')
            self.dc.find_and_tap('image/end_battle_3.png')
            print('Find end battle 3.')
            while not self.dc.find('image/next_fight.png'):
                self.dc.tap(640, 500)

            self.dc.find_and_tap('image/next_fight.png')
            print('Find next fight.')
            time.sleep(10)
            if self.dc.find('image/AP_recover.png', threshold=0.8) and i != rounds - 1:
                print('Find AP recover.')
                self.dc.find_and_tap('image/gold_apple.png', threshold=0.7)
                print('Find gold apple.')
                self.dc.find_and_tap('image/recover_decide.png')
                print('Find recover decide.')

    def red(self, pics, rounds=1):
        for i in range(rounds):
            print(f'Round {i + 1}')
            self.dc.find_and_tap('image/assassin.png')
            print('Find assassin.')

            while not any(self.dc.find(pic) for pic in pics):
                print('Waiting for friend list.')
                self.dc.swipe_screen(800, 600, 800, 400, 500)
                if self.dc.find('image/friend_end_list.png', threshold=0.92):
                    print('Friend list end.')
                    self.dc.find_and_tap('image/new_friends.png')
                    print('Find new friends.')
                    self.dc.find_and_tap('image/new_friends_check.png')
                    print('Find new friends check.')
            found_pic = next(pic for pic in pics if self.dc.find(pic))
            self.dc.find_and_tap(found_pic)
            print('Find red chara.')
            if i == 0:
                # time.sleep(3)
                # self.dc.tap(580, 40, delay=1)
                self.dc.find_and_tap('image/battle_start.png', threshold=0.7)
                print('Find battle start.')
            while not self.dc.find('image/attack.png', threshold=0.7):
                time.sleep(1)
                pass

            self.dc.tap_skill(1, 2, choose=2, delay=1)
            self.dc.tap_skill(1, 3, choose=2, delay=1)
            self.dc.tap_skill(3, 2, choose=2, delay=1)
            self.dc.tap_skill(3, 3, choose=2, delay=1)
            self.dc.tap_QQ_skill(1, 1, choose=0, delay=1)
            self.dc.tap_QQ_skill(3, 2, choose=0, delay=1)


            self.dc.find_and_tap('image/attack.png')
            print('Find attack.')
            self.dc.tap(640, 300)
            self.dc.tap(640, 500)
            self.dc.tap(850, 500)

            while not self.dc.find('image/attack.png', threshold=0.7):
                time.sleep(1)
                pass
            self.dc.tap_QQ_skill(2, 1, choose=0, delay=1)
            self.dc.tap_skill(1, 1, choose=2, delay=1)


            self.dc.find_and_tap('image/attack.png')
            print('Find attack.')
            self.dc.tap(640, 300)
            self.dc.tap(640, 500)
            self.dc.tap(850, 500)

            while not self.dc.find('image/attack.png', threshold=0.7):
                time.sleep(1)
                pass

            self.dc.tap_skill(3, 1, choose=2, delay=1)

            self.dc.tap_people_skill(3)
            self.dc.tap_skill(3, 2, choose=2, delay=1)
            self.dc.tap_QQ_skill(1, 1, choose=0, delay=1)
            self.dc.tap_people_skill(1)
            self.dc.tap_skill(3, 1, choose=0, delay=1)
            self.dc.tap_skill(3, 3, choose=2, delay=1)
            self.dc.tap_QQ_skill(3, 2, choose=0, delay=1)


            self.dc.find_and_tap('image/attack.png')
            print('Find attack.')
            self.dc.tap(640, 300)
            self.dc.tap(640, 500)
            self.dc.tap(850, 500)
            self.dc.find_and_tap('image/end_battle.png')
            print('Find end battle.')
            self.dc.find_and_tap('image/end_battle_2.png')
            print('Find end battle 2.')
            self.main_window.count_and_add('image/material/cristal.png')
            self.dc.find_and_tap('image/end_battle_3.png')
            print('Find end battle 3.')
            while not self.dc.find('image/next_fight.png'):
                self.dc.tap(640, 500)

            self.dc.find_and_tap('image/next_fight.png')
            print('Find next fight.')
            time.sleep(10)
            if self.dc.find('image/AP_recover.png', threshold=0.8) and i != rounds - 1:
                print('Find AP recover.')
                self.dc.find_and_tap('image/gold_apple.png', threshold=0.7)
                print('Find gold apple.')
                self.dc.find_and_tap('image/recover_decide.png')
                print('Find recover decide.')