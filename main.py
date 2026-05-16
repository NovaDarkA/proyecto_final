#contra seña del login y usuario: usuario admin y contraseña admin123
import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPalette

from database_connection import Connection
from LoginController import loginControler
from GestióndeVideojuegosController import GestiVideoGame
from VentasController import ventas
from ReportesController import reportes
from DashboardController import DashboardController


class LoginDialo(QtWidgets.QMainWindow):
    login_sucessFull = pyqtSignal()

    def __init__(self, manager):
        super().__init__()
        uic.loadUi("./views/1Login.ui", self)
        self.controllerrs = loginControler(self, manager)


class Sell(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("views/2Dashboard.ui", self)


class AppManager:
    def __init__(self):
        self.db = Connection()
        self.db.connect()

        self.empleado_activo = {}

        self.login_window = LoginDialo(self)
        self.sell_window = Sell()

        self.login_window.login_sucessFull.connect(self.show_main_window)
        self.login_window.show()

    def show_main_window(self):
        self.sell_window.show()
        self.dash_controller = DashboardController(self.sell_window, self)
        self.games_controller = GestiVideoGame(self, self.sell_window, self)
        self.ventas_gamer = ventas(self.sell_window, self)
        self.reportes_ctrl = reportes(self.sell_window, self)
        self.sell_window.btnLogout.clicked.connect(self.handle_logout)
        self.login_window.close()

    def handle_logout(self):
        self.empleado_activo = {}
        self.sell_window.hide()
        self.login_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    manager = AppManager()
    sys.exit(app.exec())