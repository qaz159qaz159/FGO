import time
class FGOscript:
    def __init__(self, device_controller):
        self.dc = device_controller

    def money(self, rounds=1):
        self.dc.take_screenshot()
        for i in range(rounds):
            print(f'Round {i + 1}')
            self.dc.find_and_tap('image/wizard.png')
            print('Find wizard.')
            while not self.dc.find('image/c_caster_qp1.png') and not self.dc.find('image/c_caster_qp2.png') and not self.dc.find('image/c_caster_qp3.png'):
                print('Waiting for friend list.')
                self.dc.swipe_screen(800, 600, 800, 400, 500)
                if self.dc.find('image/friend_end_list.png', threshold=0.92):
                    print('Friend list end.')
                    self.dc.find_and_tap('image/new_friends.png')
                    print('Find new friends.')
                    self.dc.find_and_tap('image/new_friends_check.png')
                    print('Find new friends check.')
            if self.dc.find('image/c_caster_qp1.png'):
                self.dc.find_and_tap('image/c_caster_qp1.png')
            elif self.dc.find('image/c_caster_qp2.png'):
                self.dc.find_and_tap('image/c_caster_qp2.png')
            elif self.dc.find('image/c_caster_qp3.png'):
                self.dc.find_and_tap('image/c_caster_qp3.png')
            print('Find blue money chara.')
            if i == 0:
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
            self.dc.find_and_tap('image/end_battle_3.png')
            print('Find end battle 3.')
            self.dc.find_and_tap('image/next_fight.png')
            print('Find next fight.')
            time.sleep(10)
            if self.dc.find('image/AP_recover.png', threshold=0.8):
                print('Find AP recover.')
                self.dc.find_and_tap('image/gold_apple.png', threshold=0.7)
                print('Find gold apple.')
                self.dc.find_and_tap('image/recover_decide.png')
                print('Find recover decide.')

    @staticmethod
    def counter():
        pass
