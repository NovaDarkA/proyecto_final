from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import (
    QTableWidgetItem,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)


class GestiVideoGame:
    def __init__(self, manager, window, model):
        self.manager = manager
        self.window = window
        self.model = model

        self.games_window = None
        self.juego_seleccionado = None

        self.window.btnGames.clicked.connect(self.handle_games)

    def handle_games(self):
        if self.games_window is None:
            self.games_window = uic.loadUi("./views/3gestigames.ui")

            self.games_window.btnAdd.clicked.connect(self.regresar_dashboard)
            self.games_window.btnEdit.clicked.connect(self.modificar_juego)
            self.games_window.btnDelete.clicked.connect(self.eliminar_juego)

            self.games_window.tblGames.clicked.connect(self.cargar_seleccion)

        self.juego_seleccionado = None

        self.cargar_tabla()

        self.window.hide()
        self.games_window.show()

    def cargar_tabla(self):
        sql = """
            SELECT
                id_juego,
                titulo,
                plataforma,
                genero,
                precio,
                stock
            FROM videojuegos
            WHERE activo = 1
        """

        filas = self.manager.db.select(sql)

        tabla = self.games_window.tblGames

        tabla.setRowCount(len(filas))

        for row_idx, fila in enumerate(filas):
            for col_idx, valor in enumerate(fila):
                tabla.setItem(
                    row_idx,
                    col_idx,
                    QTableWidgetItem(str(valor))
                )

    def cargar_seleccion(self):
        tabla = self.games_window.tblGames

        fila = tabla.currentRow()

        if fila < 0:
            return

        self.juego_seleccionado = {
            "id": tabla.item(fila, 0).text(),
            "titulo": tabla.item(fila, 1).text(),
            "plataforma": tabla.item(fila, 2).text(),
            "genero": tabla.item(fila, 3).text(),
            "precio": tabla.item(fila, 4).text(),
            "stock": tabla.item(fila, 5).text(),
        }

    def modificar_juego(self):
        if not self.juego_seleccionado:
            QMessageBox.warning(
                self.games_window,
                "Gamestore",
                "Selecciona un juego de la tabla primero."
            )
            return

        dlg = QDialog(self.games_window)
        dlg.setWindowTitle("Editar Videojuego")

        layout = QVBoxLayout(dlg)

        campos = {}

        datos = [
            ("Título", "titulo"),
            ("Plataforma", "plataforma"),
            ("Género", "genero"),
            ("Precio", "precio"),
            ("Stock", "stock")
        ]

        for etiqueta, key in datos:
            row = QHBoxLayout()

            row.addWidget(QLabel(etiqueta + ":"))

            txt = QLineEdit(self.juego_seleccionado[key])

            campos[key] = txt

            row.addWidget(txt)

            layout.addLayout(row)

        btn_guardar = QPushButton("Guardar")

        layout.addWidget(btn_guardar)

        def guardar():
            sql = """
                UPDATE videojuegos
                SET
                    titulo = ?,
                    plataforma = ?,
                    genero = ?,
                    precio = ?,
                    stock = ?
                WHERE id_juego = ?
            """

            vals = (
                campos["titulo"].text(),
                campos["plataforma"].text(),
                campos["genero"].text(),
                float(campos["precio"].text()),
                int(campos["stock"].text()),
                int(self.juego_seleccionado["id"])
            )

            rows = self.manager.db.update(sql, vals)

            if rows:
                QMessageBox.information(
                    dlg,
                    "Gamestore",
                    "Juego actualizado correctamente."
                )

                dlg.accept()

                self.cargar_tabla()

        btn_guardar.clicked.connect(guardar)

        dlg.exec()

    def eliminar_juego(self):
        if not self.juego_seleccionado:
            QMessageBox.warning(
                self.games_window,
                "Gamestore",
                "Selecciona un juego de la tabla primero."
            )
            return

        confirm = QMessageBox.question(
            self.games_window,
            "Confirmar",
            f"¿Eliminar '{self.juego_seleccionado['titulo']}'?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            sql = """
                UPDATE videojuegos
                SET activo = 0
                WHERE id_juego = ?
            """

            rows = self.manager.db.update(
                sql,
                (int(self.juego_seleccionado["id"]),)
            )

            if rows:
                QMessageBox.information(
                    self.games_window,
                    "Gamestore",
                    "Juego eliminado."
                )

                self.juego_seleccionado = None

                self.cargar_tabla()

    def regresar_dashboard(self):
        self.games_window.hide()
        self.window.show()