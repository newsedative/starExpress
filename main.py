import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QCheckBox, QLabel
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
import sqlite3

spisok = []


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('welcomescreen.ui', self)  # Загружаем дизайн
        self.login_pushbutton.clicked.connect(self.gotologinscreen)
        self.signup_pushbutton.clicked.connect(self.gotosignupscreen)

    def gotologinscreen(self):  # переход к окну входа
        self.login = LoginScreen()
        self.login.setFixedWidth(1200)
        self.login.setFixedHeight(800)
        self.login.show()
        self.close()

    def gotosignupscreen(self):  # переход к окну регистрации
        self.signup = SignUpScreen()
        self.signup.show()
        self.close()


class LoginScreen(QMainWindow):   # окно входа
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Password)  # скрытие пароля
        self.loginButton.clicked.connect(self.loginfunc)
        self.gobackButton.clicked.connect(self.goback)

    def loginfunc(self):
        email = self.lineEditEmail.text()
        password = self.lineEditPassword.text()

        if len(email) == 0 or len(password) == 0:  # проверка, заполненны ли все поля
            self.label_4.setText('Вы заполнили не все поля')
        else:
            try:
                con = sqlite3.connect('appDB.db')  # подключение к базе данным
                cur = con.cursor()
                # поиск логина и пароля
                cur.execute('SELECT password FROM empinfo WHERE login = "{}"'.format(email))
                dbPassword = cur.fetchone()[0]
                con.close()
                if dbPassword != password:  # проверка правильности пароля
                    self.label_4.setText('Неправильный пароль или логин')
                else:
                    print('Вход выполнен успешно')
                    self.label_4.setText('')
                    # переход к окну магазина
                    self.shop = ShopScreen()
                    self.shop.setFixedWidth(1200)
                    self.shop.setFixedHeight(800)
                    self.shop.show()
                    self.close()
            except TypeError:
                self.label_4.setText('Неправильный пароль или логин')

    def goback(self):
        self.welcome = MyWidget()
        self.welcome.show()
        self.welcome.setFixedWidth(1200)
        self.welcome.setFixedHeight(800)
        self.close()


class SignUpScreen(QMainWindow):  # окно регистрации
    def __init__(self):
        super().__init__()
        uic.loadUi('signup.ui', self)
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Password) # скрытие пароля
        self.lineEditPassword2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signupButton.clicked.connect(self.regfunc)
        self.gobackButton.clicked.connect(self.goback)
        self.rulesButton.clicked.connect(self.rules)

    def regfunc(self):
        email = self.lineEditEmail.text()
        password = self.lineEditPassword.text()
        password2 = self.lineEditPassword2.text()
        # проверка
        if len(email) == 0 or len(password) == 0 or len(password2) == 0:
            self.errorLabel.setText('Вы заполнили не все поля')
        elif password != password2:
            self.errorLabel.setText('Пароли не совпадают')
        else:
            self.errorLabel.setText('')
            con = sqlite3.connect('appDB.db')
            cur = con.cursor()
            # запись email и пароля в базу данных
            cur.execute('INSERT INTO empinfo(login, password) VALUES("{}", "{}")'.format(email, password))
            con.commit()
            con.close()
            self.shop = ShopScreen()
            self.shop.setFixedWidth(1200)
            self.shop.setFixedHeight(800)
            self.shop.show()
            self.close()

    def goback(self):
        self.welcome = MyWidget()
        self.welcome.show()
        self.welcome.setFixedWidth(1200)
        self.welcome.setFixedHeight(800)
        self.close()

    def rules(self):
        self.r = RulesScr()
        self.r.show()


class RulesScr(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 300, 400, 400)
        self.plan = QPlainTextEdit(self)
        self.plan.move(20, 20)
        self.plan.resize(360, 360)
        self.plan.setReadOnly(True)
        with open('rules.txt', encoding='utf8') as f:
            f1 = f.read().split('\n')
            for elem in f1:
                self.plan.insertPlainText(elem)
                self.plan.insertPlainText('\n')


class ShopScreen(QMainWindow): # окно магазина
    def __init__(self):
        super().__init__()
        uic.loadUi('shopscreen.ui', self)
        self.pushButtonPlanet.clicked.connect(self.goToPlanetSc)
        self.pushButtonStar.clicked.connect(self.goToStarSc)
        self.pushButtonMeteorite.clicked.connect(self.gotoMeteorSc)

    def goToPlanetSc(self):
        self.planet = ShopPlanets()
        self.planet.setFixedWidth(1200)
        self.planet.setFixedHeight(800)
        self.planet.show()
        self.close()

    def goToStarSc(self):
        self.star = ShopeStars()
        self.star.setFixedWidth(1200)
        self.star.setFixedHeight(800)
        self.star.show()
        self.close()

    def gotoMeteorSc(self):
        self.meteorits = ShopeMeteorits()
        self.meteorits.setFixedWidth(1200)
        self.meteorits.setFixedHeight(800)
        self.meteorits.show()
        self.close()


class Basket: # запись выбранных товаров
    def __init__(self, sp):
        global spisok
        self.sp = sp.split()

    def print(self):
        spisok.append(self.sp)


class ShopPlanets(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('planets.ui', self)
        self.gobackButton.clicked.connect(self.goback)
        self.appendButton.clicked.connect(self.append)
        self.goToCheckButton.clicked.connect(self.check)
        try:
            for button in self.buttonGroup.buttons():
                button.clicked.connect(self.run)
        except Exception as e:
            print(e)

    def append(self):
        basket = Basket(self.stroka)
        basket.print()

    def run(self):
        button = QWidget.sender(self)
        buttonName = button.text()
        con = sqlite3.connect('appDB.db')
        cur = con.cursor()
        cur.execute('SELECT price FROM count WHERE name = "{}"'.format(buttonName))
        price = cur.fetchone()[0]
        self.stroka = f"{buttonName} {price}"
        con.commit()
        con.close()

    def goback(self):
        self.shop = ShopScreen()
        self.shop.show()
        self.close()

    def check(self):
        self.check = Check()
        self.check.show()
        self.close()


class ShopeStars(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('stars.ui', self)
        self.goToCheckButton.clicked.connect(self.check)
        self.gobackButton.clicked.connect(self.goback)
        self.appendButton.clicked.connect(self.append)
        try:
            for button in self.buttonGroup.buttons():
                button.clicked.connect(self.run)
        except Exception as e:
            print(e)

    def append(self):
        check = Basket(self.stroka)
        check.print()

    def run(self):
        button = QWidget.sender(self)
        buttonName = button.text()
        con = sqlite3.connect('appDB.db')
        cur = con.cursor()
        cur.execute('SELECT price FROM count WHERE name = "{}"'.format(buttonName))
        price = cur.fetchone()[0]
        self.stroka = f"{buttonName} {price}"
        con.commit()
        con.close()

    def goback(self):
        self.shop = ShopScreen()
        self.shop.show()
        self.close()

    def check(self):
        self.check = Check()
        self.check.show()
        self.close()


class ShopeMeteorits(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('meteorits.ui', self)
        self.goToCheckButton.clicked.connect(self.check)
        self.gobackButton.clicked.connect(self.goback)
        self.appendButton.clicked.connect(self.append)
        try:
            for button in self.buttonGroup.buttons():
                button.clicked.connect(self.run)
        except Exception as e:
            print(e)

    def append(self):
        check = Basket(self.stroka)
        check.print()

    def run(self):
        button = QWidget.sender(self)
        buttonName = button.text()
        con = sqlite3.connect('appDB.db')
        cur = con.cursor()
        cur.execute('SELECT price FROM count WHERE name = "{}"'.format(buttonName))
        price = cur.fetchone()[0]
        self.stroka = f"{buttonName} {price}"
        con.commit()
        con.close()

    def goback(self):
        self.shop = ShopScreen()
        self.shop.show()
        self.close()

    def check(self):
        self.check = Check()
        self.check.show()
        self.close()


class Check(QWidget):
    def __init__(self):
        # Надо не забыть вызвать инициализатор базового класса
        super().__init__()
        # В метод initUI() будем выносить всю настройку интерфейса
        # чтобы не перегружать инициализатор
        self.initUI()
        global spisok

    def initUI(self):
        try:
            # Зададим размер и положение нашего виджета
            self.setGeometry(400, 300, 400, 400)
            x = 20
            y = 20
            sum = 0
            for p in spisok:
                sum += int(p[1])
                self.chB = QCheckBox(p[0], self)
                self.chB.move(x, y)
                self.chB.clicked.connect(self.send2)
                y += 30
            self.label = QLabel(self)
            self.label.setText(f"Итого: {sum}")
            self.label.move(x, y)
            print(sum)
        except Exception as e:
            print(e)

    def send2(self):
        n = QWidget.sender(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.setFixedWidth(1200)
    ex.setFixedHeight(800)
    ex.show()
    sys.exit(app.exec_())