from PyQt6 import QtWidgets


class loginControler:
    def __init__(self, window, manager):
        self.window = window
        self.manager = manager

        self.window.btnLogin.clicked.connect(self.handle_login)

    def handle_login(self):
        usuario = self.window.txtUser.text().strip()
        contrasena = self.window.txtPass.text().strip()

        if not usuario or not contrasena:
            QtWidgets.QMessageBox.warning(
                self.window,
                "Gamestore Manager",
                "Por favor ingresa usuario y contraseña."
            )
            return

        sql = """
            SELECT
                id_empleado,
                nombre,
                rol
            FROM empleados
            WHERE usuario = ?
            AND contrasena = ?
            AND activo = 1
        """

        results = self.manager.db.select(
            sql,
            (usuario, contrasena)
        )

        if results:
            empleado = results[0]

            self.manager.empleado_activo = {
                "id": empleado[0],
                "nombre": empleado[1],
                "rol": empleado[2],
            }

            self.window.login_sucessFull.emit()

        else:
            QtWidgets.QMessageBox.warning(
                self.window,
                "Gamestore Manager - Error",
                "Usuario o contraseña incorrectos."
            )