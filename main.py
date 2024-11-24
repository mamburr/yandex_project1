import sqlite3
import sys
import time
import threading
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLCDNumber, QLabel, QMainWindow
import random as r
from PyQt6 import uic

app = QApplication(sys.argv)

PET_NAME = ''

info = {'money': 0, 'food': 0, 'water': 0, 'health': 0}


class Start(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('start_menu.ui', self)
        self.initUI()

    def initUI(self):
        self.login.clicked.connect(self.logging)
        self.registration.clicked.connect(self.registr)

    def logging(self):
        global PET_NAME
        name = self.name_input.text()
        if name in db.get_pets():
            self.parent().main_screen.show()
            self.parent().set_window_size(791, 540)
            self.hide()
            ticks.start()
            PET_NAME = name
        else:
            self.error_photo.setPixmap(QPixmap("error.png"))
            self.error.setText('Такого питомца не существует!')

    def registr(self):
        global PET_NAME
        name = self.name_input.text()
        if name not in db.get_pets():
            db.new_pet(name)
            self.parent().main_screen.show()
            self.parent().set_window_size(791, 540)
            self.hide()
            ticks.start()
            PET_NAME = name
        else:
            self.error_photo.setPixmap(QPixmap("error.png"))
            self.error.setText('Такой питомец уже существует!')


class Main(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('new_main_menu.ui', self)
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 791, 540)
        self.background.setPixmap(QPixmap('house_1.jpg'))
        self.pet.setPixmap(QPixmap('kvadrober.png'))
        self.money_photo.setPixmap(QPixmap('money.png'))
        self.health_photo.setPixmap(QPixmap('lifes.png'))
        self.food_photo.setPixmap(QPixmap('food1.png'))
        self.water_photo.setPixmap(QPixmap('water.png'))
        self.shop_btn.setIcon(QIcon('shop.png'))
        self.games_btn.setIcon(QIcon('games.png'))
        self.games_btn.clicked.connect(self.select_game)
        self.shop_btn.clicked.connect(self.shopping)

    def shopping(self):
        ticks.paused()
        self.parent().shop_screen.show()
        self.parent().set_window_size(359, 248)
        MainWindow.shop_screen.update_bar()
        self.hide()

    def select_game(self):
        ticks.paused()
        self.parent().game_menu_screen.show()
        self.parent().set_window_size(390, 182)
        self.hide()

    def label_update(self):
        self.money.setText(str(info['money']))
        self.health.setText(str(info['health']))
        self.food.setText(str(info['food']))
        self.water.setText(str(info['water']))


class Shop(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('shop.ui', self)
        self.initUI()

    def initUI(self):
        self.money_photo.setPixmap(QPixmap('money.png'))
        self.food_photo.setPixmap(QPixmap('food1.png'))
        self.water_photo.setPixmap(QPixmap('water.png'))
        self.close.setIcon(QIcon('close.png'))
        self.whiskas.setIcon(QIcon('whiskas.png'))
        self.cucumber.setIcon(QIcon('cucumber.png'))
        self.grass.setIcon(QIcon('grass.png'))
        self.bottle.setIcon(QIcon('bottle.png'))
        self.money_photo_2.setPixmap(QPixmap('money.png'))
        self.money_photo_3.setPixmap(QPixmap('money.png'))
        self.money_photo_4.setPixmap(QPixmap('money.png'))
        self.money_photo_5.setPixmap(QPixmap('money.png'))
        self.whiskas.clicked.connect(self.buy_whiskas)
        self.cucumber.clicked.connect(self.buy_cucumber)
        self.grass.clicked.connect(self.buy_grass)
        self.bottle.clicked.connect(self.buy_bottle)
        self.close.clicked.connect(self.switch_main)

    def switch_main(self):
        ticks.paused()
        self.parent().main_screen.show()
        self.parent().set_window_size(791, 540)
        self.warning.setHidden(True)
        self.warning_photo.setHidden(True)
        self.hide()

    def update_bar(self):
        self.money.setText(str(info['money']))
        self.food.setText(str(info['food']))
        self.water.setText(str(info['water']))

    def raise_error(self):
        self.warning.setHidden(False)
        self.warning_photo.setHidden(False)
        self.warning_photo.setPixmap(QPixmap('error.png'))
        self.warning.setText("Недостаточно денег")

    def buy_whiskas(self):
        self.warning.setHidden(True)
        self.warning_photo.setHidden(True)
        if info['money'] > 25:
            if info['food'] + 50 > 100:
                info['food'] = 100
            else:
                info['food'] += 50
            info['money'] -= 25
            db.update_info()
            self.update_bar()
        else:
            self.raise_error()

    def buy_cucumber(self):
        self.warning.setHidden(True)
        self.warning_photo.setHidden(True)
        if info['money'] > 15:
            if info['food'] + 25 > 100:
                info['food'] = 100
            else:
                info['food'] += 25
            info['money'] -= 15
            db.update_info()
            self.update_bar()
        else:
            self.raise_error()

    def buy_grass(self):
        self.warning.setHidden(True)
        self.warning_photo.setHidden(True)
        if info['money'] > 5:
            if info['food'] + 8 > 100:
                info['food'] = 100
            else:
                info['food'] += 8
            info['money'] -= 5
            db.update_info()
            self.update_bar()
        else:
            self.raise_error()

    def buy_bottle(self):
        self.warning.setHidden(True)
        self.warning_photo.setHidden(True)
        if info['money'] > 15:
            if info['water'] + 25 > 100:
                info['water'] = 100
            else:
                info['water'] += 25
            info['money'] -= 15
            db.update_info()
            self.update_bar()
        else:
            self.raise_error()


class Games(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('select_game.ui', self)
        self.money.setHidden(True)
        self.money_photo.setHidden(True)
        self.initUI()

    def initUI(self):
        self.close.setIcon(QIcon('close.png'))
        self.close.clicked.connect(self.switch_to_main)
        self.game1.clicked.connect(self.switch_to_game1)
        self.game2.clicked.connect(self.switch_to_game2)
        self.game3.clicked.connect(self.switch_to_game3)

    def switch_to_main(self):
        ticks.paused()
        self.parent().main_screen.show()
        self.parent().set_window_size(791, 540)
        self.money.setHidden(True)
        self.money_photo.setHidden(True)
        self.hide()

    def switch_to_game1(self):
        self.parent().game1_screen.show()
        self.parent().set_window_size(424, 143)
        self.money.setHidden(True)
        self.money_photo.setHidden(True)
        self.hide()

    def earned_money(self, money):
        self.money.setHidden(False)
        self.money_photo.setHidden(False)
        self.money.setText('+' + str(money))
        self.money_photo.setPixmap(QPixmap('money.png'))

    def switch_to_game2(self):
        self.parent().game2_screen.show()
        MainWindow.game2_screen.update_money()
        self.parent().set_window_size(538, 186)
        self.money.setHidden(True)
        self.money_photo.setHidden(True)
        self.hide()

    def switch_to_game3(self):
        self.parent().game3_screen.show()
        MainWindow.game3_screen.update_money()
        self.parent().set_window_size(409, 406)
        self.money.setHidden(True)
        self.money_photo.setHidden(True)
        self.hide()


class Game_1(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('game1.ui', self)
        self.numbers = [i for i in range(1, 11)]
        r.shuffle(self.numbers)
        self.count = 1
        self.initUI()

    def initUI(self):
        self.close.setIcon(QIcon('close.png'))
        self.close.clicked.connect(self.switch_to_game_select)
        for i in range(10):
            exec(f'self.btn{i + 1}.setText(str(self.numbers[i]))')
            exec(f'self.btn{i + 1}.clicked.connect(self.btn{i + 1}_click)')

    def btn1_click(self):
        if self.btn1.text() == str(self.count):
            self.count += 1
            self.btn1.hide()
            self.win_check()

    def btn2_click(self):
        if self.btn2.text() == str(self.count):
            self.count += 1
            self.btn2.hide()
            self.win_check()

    def btn3_click(self):
        if self.btn3.text() == str(self.count):
            self.count += 1
            self.btn3.hide()
            self.win_check()

    def btn4_click(self):
        if self.btn4.text() == str(self.count):
            self.count += 1
            self.btn4.hide()
            self.win_check()

    def btn5_click(self):
        if self.btn5.text() == str(self.count):
            self.count += 1
            self.btn5.hide()
            self.win_check()

    def btn6_click(self):
        if self.btn6.text() == str(self.count):
            self.count += 1
            self.btn6.hide()
            self.win_check()

    def btn7_click(self):
        if self.btn7.text() == str(self.count):
            self.count += 1
            self.btn7.hide()
            self.win_check()

    def btn8_click(self):
        if self.btn8.text() == str(self.count):
            self.count += 1
            self.btn8.hide()
            self.win_check()

    def btn9_click(self):
        if self.btn9.text() == str(self.count):
            self.count += 1
            self.btn9.hide()
            self.win_check()

    def btn10_click(self):
        if self.btn10.text() == str(self.count):
            self.count += 1
            self.btn10.hide()
            self.win_check()

    def win_check(self):
        if self.count == 11:
            r.shuffle(self.numbers)
            for i in range(10):
                exec(f'self.btn{i + 1}.show()')
                exec(f'self.btn{i + 1}.setText(str(self.numbers[i]))')
            MainWindow.game_menu_screen.earned_money(10)
            self.count = 1
            self.parent().game_menu_screen.show()
            self.parent().set_window_size(390, 182)
            self.hide()
            info['money'] += 10
            db.update_info()
            MainWindow.main_screen.label_update()

    def switch_to_game_select(self):
        self.parent().game_menu_screen.show()
        self.parent().set_window_size(390, 182)
        self.hide()


class Game_2(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('game2.ui', self)
        self.initUI()

    def initUI(self):
        self.close.setIcon(QIcon('close.png'))
        self.close.clicked.connect(self.switch_to_game_select)
        self.money_photo.setPixmap(QPixmap('money.png'))
        self.play.clicked.connect(self.make_bet)
        self.rock.clicked.connect(self.rock_click)
        self.scissors.clicked.connect(self.scissors_click)
        self.papper.clicked.connect(self.papper_click)
        self.bot_variants = ['камень', "ножницы", "бумага"]
        self.start = False

    def make_bet(self):
        if not self.start:
            if self.bet.text():
                self.bet_money = int(self.bet.text())
                if self.bet_money <= 0:
                    self.warning.setHidden(False)
                    self.warning_photo.setHidden(False)
                    self.warning_photo.setPixmap(QPixmap('error.png'))
                    self.warning.setText("Ставка <= 0")
                    self.warning.setGeometry(420, 140, 101, 20)
                    self.warning_photo.setGeometry(370, 133, 31, 31)
                elif self.bet_money > db.get_info()[0]:
                    self.warning.setHidden(False)
                    self.warning_photo.setHidden(False)
                    self.warning_photo.setPixmap(QPixmap('error.png'))
                    self.warning.setText("Недостаточно денег")
                    self.warning.setGeometry(370, 140, 161, 20)
                    self.warning_photo.setGeometry(330, 130, 31, 31)
                else:
                    self.bot_choice = r.choice(self.bot_variants)
                    self.start = True
                    self.warning.setHidden(True)
                    self.warning_photo.setHidden(True)
                    self.result.setText("Игра началась")
            else:
                self.warning.setHidden(False)
                self.warning_photo.setHidden(False)
                self.warning_photo.setPixmap(QPixmap('error.png'))
                self.warning.setText("Введите значение")
                self.warning.setGeometry(370, 140, 161, 20)
                self.warning_photo.setGeometry(330, 130, 31, 31)
        else:
            self.warning.setHidden(False)
            self.warning_photo.setHidden(False)
            self.warning_photo.setPixmap(QPixmap('error.png'))
            self.warning.setText("Игра еще идёт")
            self.warning.setGeometry(370, 140, 161, 20)
            self.warning_photo.setGeometry(330, 130, 31, 31)

    def rock_click(self):
        if self.bot_choice == 'ножницы':
            self.win()
        elif self.bot_choice == "бумага":
            self.lose()
        elif self.bot_choice == "камень":
            self.draw()

    def scissors_click(self):
        if self.bot_choice == 'бумага':
            self.win()
        elif self.bot_choice == "камень":
            self.lose()
        elif self.bot_choice == "ножницы":
            self.draw()

    def papper_click(self):
        if self.bot_choice == 'камень':
            self.win()
        elif self.bot_choice == "ножницы":
            self.lose()
        elif self.bot_choice == "бумага":
            self.draw()

    def win(self):
        if self.start:
            self.result.setHidden(False)
            self.result.setText('Ты выйграл!')
            info['money'] += self.bet_money
            db.update_info()
            self.update_money()
            self.start = False
        else:
            self.warning.setHidden(False)
            self.warning_photo.setHidden(False)
            self.warning_photo.setPixmap(QPixmap('error.png'))
            self.warning.setText("Сделай ставку!")
            self.warning.setGeometry(370, 140, 161, 20)
            self.warning_photo.setGeometry(330, 130, 31, 31)

    def lose(self):
        if self.start:
            self.result.setHidden(False)
            self.result.setText('Ты проиграл!')
            info['money'] -= self.bet_money
            db.update_info()
            self.update_money()
            self.start = False
        else:
            self.warning.setHidden(False)
            self.warning_photo.setHidden(False)
            self.warning_photo.setPixmap(QPixmap('error.png'))
            self.warning.setText("Сделай ставку!")
            self.warning.setGeometry(370, 140, 161, 20)
            self.warning_photo.setGeometry(330, 130, 31, 31)

    def draw(self):
        if self.start:
            self.result.setHidden(False)
            self.result.setText('Ничья, выбирай еще раз')
            self.bot_choice = r.choice(self.bot_variants)

    def switch_to_game_select(self):
        self.parent().game_menu_screen.show()
        self.hide()
        self.parent().set_window_size(390, 182)

    def update_money(self):
        self.money.setText(str(db.get_info()[0]))


class Game_3(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('game3.ui', self)
        self.initUI()

    def initUI(self):
        self.close.setIcon(QIcon('close.png'))
        self.money_photo.setPixmap(QPixmap('money.png'))
        for i in range(9):
            exec(f'self.btn_{i + 1}.clicked.connect(self.btn_{i + 1}_click)')
        self.btn_1.setIcon(QIcon('one.png'))
        self.btn_2.setIcon(QIcon('two.png'))
        self.btn_3.setIcon(QIcon('three.png'))
        self.btn_4.setIcon(QIcon('four.png'))
        self.btn_5.setIcon(QIcon('five.png'))
        self.btn_6.setIcon(QIcon('six.png'))
        self.btn_7.setIcon(QIcon('seven.png'))
        self.btn_8.setIcon(QIcon('eight.png'))
        self.btn_9.setIcon(QIcon('nine.png'))
        self.play.clicked.connect(self.make_bet)
        self.close.clicked.connect(self.swith_to_game_select)
        self.collect.clicked.connect(self.collect_money)
        self.start = False
        self.count = 0
        self.combination = []
        self.round = 1
        self.pressed = 0
        self.koeficent = 1

    def swith_to_game_select(self):
        self.parent().game_menu_screen.show()
        self.parent().set_window_size(390, 182)
        self.hide()

    def make_bet(self):
        if not self.start:
            if self.bet.text():
                self.bet_money = int(self.bet.text())
                if self.bet_money <= 0:
                    self.warning.setHidden(False)
                    self.warning_photo.setHidden(False)
                    self.warning_photo.setPixmap(QPixmap('error.png'))
                    self.warning.setText("Ставка <= 0")
                elif self.bet_money > db.get_info()[0]:
                    self.warning.setHidden(False)
                    self.warning_photo.setHidden(False)
                    self.warning_photo.setPixmap(QPixmap('error.png'))
                    self.warning.setText("Недостаточно денег")
                else:
                    self.start = True
                    self.warning.setHidden(False)
                    self.warning_photo.setHidden(True)
                    self.combination = []
                    self.combination.append(r.randint(1, 9))
                    self.warning.setText("Игра началась")
                    self.result.setText(str(self.combination[0]))
                    self.koef.setText(f'{self.koeficent}x')
            else:
                self.warning.setHidden(False)
                self.warning_photo.setHidden(False)
                self.warning_photo.setPixmap(QPixmap('error.png'))
                self.warning.setText("Введите значение")
        else:
            self.warning.setHidden(False)
            self.warning_photo.setHidden(False)
            self.warning_photo.setPixmap(QPixmap('error.png'))
            self.warning.setText("Игра еще идёт")

    def update_money(self):
        self.money.setText(str(db.get_info()[0]))

    def btn_1_click(self):
        self.pressed = 1
        if self.start:
            self.result.setHidden(True)
            if self.combination[self.count] == self.pressed:
                self.count_check = self.count
                self.count += 1
                if self.combination[self.count_check] == self.combination[-1] and self.count_check == len(
                        self.combination) - 1:
                    self.next_round()
            else:
                self.lose()

    def btn_2_click(self):
        self.pressed = 2
        if self.start:
            self.result.setHidden(True)
            if self.combination[self.count] == self.pressed:
                self.count_check = self.count
                self.count += 1
                if self.combination[self.count_check] == self.combination[-1] and self.count_check == len(
                        self.combination) - 1:
                    self.next_round()
            else:
                self.lose()

    def btn_3_click(self):
        self.pressed = 3
        if self.start:
            self.result.setHidden(True)
            if self.combination[self.count] == self.pressed:
                self.count_check = self.count
                self.count += 1
                if self.combination[self.count_check] == self.combination[-1] and self.count_check == len(
                        self.combination) - 1:
                    self.next_round()
            else:
                self.lose()

    def btn_4_click(self):
        self.pressed = 4
        if self.start:
            self.result.setHidden(True)
            if self.combination[self.count] == self.pressed:
                self.count_check = self.count
                self.count += 1
                if self.combination[self.count_check] == self.combination[-1] and self.count_check == len(
                        self.combination) - 1:
                    self.next_round()
            else:
                self.lose()

    def btn_5_click(self):
        self.pressed = 5
        if self.start:
            self.result.setHidden(True)
            if self.combination[self.count] == self.pressed:
                self.count_check = self.count
                self.count += 1
                if self.combination[self.count_check] == self.combination[-1] and self.count_check == len(
                        self.combination) - 1:
                    self.next_round()
            else:
                self.lose()

    def btn_6_click(self):
        self.pressed = 6
        if self.start:
            self.result.setHidden(True)
            if self.combination[self.count] == self.pressed:
                self.count_check = self.count
                self.count += 1
                if self.combination[self.count_check] == self.combination[-1] and self.count_check == len(
                        self.combination) - 1:
                    self.next_round()
            else:
                self.lose()

    def btn_7_click(self):
        self.pressed = 7
        if self.start:
            self.result.setHidden(True)
            if self.combination[self.count] == self.pressed:
                self.count_check = self.count
                self.count += 1
                if self.combination[self.count_check] == self.combination[-1] and self.count_check == len(
                        self.combination) - 1:
                    self.next_round()
            else:
                self.lose()

    def btn_8_click(self):
        self.pressed = 8
        if self.start:
            self.result.setHidden(True)
            if self.combination[self.count] == self.pressed:
                self.count_check = self.count
                self.count += 1
                if self.combination[self.count_check] == self.combination[-1] and self.count_check == len(
                        self.combination) - 1:
                    self.next_round()
            else:
                self.lose()

    def btn_9_click(self):
        self.pressed = 9
        if self.start:
            self.result.setHidden(True)
            if self.combination[self.count] == self.pressed:
                self.count_check = self.count
                self.count += 1
                if self.combination[self.count_check] == self.combination[-1] and self.count_check == len(
                        self.combination) - 1:
                    self.next_round()
            else:
                self.lose()

    def collect_money(self):
        if self.start:
            self.start = False
            self.result.setHidden(False)
            self.result.setText('Вы забрали деньги!')
            info['money'] += int(self.bet_money * (self.koeficent - 1))
            print(int(self.bet_money * (self.koeficent - 1)), self.koeficent)
            db.update_info()
            self.update_money()
            self.koeficent = 1
            self.koef.setText(f'{self.koeficent}x')

    def lose(self):
        self.start = False
        info['money'] -= self.bet_money
        self.result.setHidden(False)
        self.result.setText('Вы проиграли')
        db.update_info()
        self.update_money()
        self.koeficent = 1
        self.koef.setText(f'{self.koeficent}x')
        self.warning.setHidden(True)
        self.count = 0
        self.round = 1

    def next_round(self):
        self.count = 0
        self.round += 1
        self.combination = [r.randint(1, 9) for i in range(self.round)]
        self.result.setHidden(False)
        self.result.setText(' '.join(list(map(str, self.combination))))
        self.koeficent = 1 + ((self.round ** 2 - self.round) / 10)
        self.koef.setText(f'{self.koeficent}x')


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.start_menu.show()

    def initUI(self):
        self.setGeometry(0, 0, 380, 296)
        self.start_menu = Start(self)
        self.start_menu.hide()
        self.main_screen = Main(self)
        self.main_screen.hide()
        self.shop_screen = Shop(self)
        self.shop_screen.hide()
        self.game_menu_screen = Games(self)
        self.game_menu_screen.hide()
        self.game1_screen = Game_1(self)
        self.game1_screen.hide()
        self.game2_screen = Game_2(self)
        self.game2_screen.hide()
        self.game3_screen = Game_3(self)
        self.game3_screen.hide()
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle('Мой Говорящий Квадробер')

    def set_window_size(self, width, height):
        self.setGeometry(100, 100, width, height)


MainWindow = Game()


class TickMaster(threading.Thread):
    def __init__(self):
        super().__init__()
        self.pause = True

    def run(self):
        self.running = True
        while self.running:
            if self.pause:
                info['money'], info['food'], info['water'], info['health'] = db.get_info()[0], db.get_info()[1], \
                    db.get_info()[2], db.get_info()[3]
                if info['food'] > 0:
                    info['food'] -= 2
                else:
                    info['food'] = 0
                    info['health'] -= 2
                if info['water'] > 0:
                    info['water'] -= 3
                else:
                    info['water'] = 0
                    info['health'] -= 2
                if info['water'] < 0:
                    info['water'] = 0
                if info['food'] < 0:
                    info['food'] = 0
                db.update_info()
                MainWindow.main_screen.label_update()
                time.sleep(10)

    def stop(self):
        self.running = False

    def paused(self):
        self.pause = not self.pause


ticks = TickMaster()


class DataBase:
    def __init__(self):
        pass

    def new_pet(self, pet):
        self.con = sqlite3.connect('dbbase.sqlite')
        self.con.execute(f"""INSERT INTO Pets (name, money,food,water,health) VALUES ('{pet}', 50,100,100,100)""")
        self.con.commit()
        self.con.close()

    def get_pets(self):
        self.con = sqlite3.connect('dbbase.sqlite')
        result = self.con.execute("""SELECT name FROM Pets""").fetchall()
        self.con.commit()
        return list(map(lambda x: x[0], result))

    def get_info(self):
        self.con = sqlite3.connect('dbbase.sqlite')
        result = self.con.execute(f"""SELECT money,food,water,health FROM Pets WHERE name='{PET_NAME}'""").fetchall()[0]
        self.con.commit()
        self.con.close()
        return result

    def update_info(self):
        self.con = sqlite3.connect('dbbase.sqlite')
        self.con.execute(
            f"""UPDATE Pets SET money={info['money']}, food={info['food']}, water={info['water']}, health={info['health']} WHERE name='{PET_NAME}'""")
        self.con.commit()
        self.con.close()


db = DataBase()

if __name__ == '__main__':
    MainWindow.show()
    sys.exit(app.exec())
