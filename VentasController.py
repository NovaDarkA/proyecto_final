from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMessageBox


class ventas:
    def __init__(self, window, manager):
        self.window = window
        self.manager = manager

        self.sales_window = None

        self.window.btnSales.clicked.connect(
            self.handle_venta
        )

    def handle_venta(self):
        if self.sales_window is None:
            self.sales_window = uic.loadUi(
                "./views/4ventas.ui"
            )

            self.sales_window.btnAdd.clicked.connect(
                self.regresar_dashboard
            )

            self.sales_window.btnRegister.clicked.connect(
                self.registrar_venta
            )

        self.cargar_juegos()

        self.window.hide()
        self.sales_window.show()

    def cargar_juegos(self):
        sql = """
            SELECT
                id_juego,
                titulo,
                precio
            FROM videojuegos
            WHERE activo = 1
            AND stock > 0
        """

        juegos = self.manager.db.select(sql)

        combo = self.sales_window.cmbGame

        combo.clear()

        for juego in juegos:
            combo.addItem(
                f"{juego[1]} (${juego[2]})",
                juego[0]
            )

    def registrar_venta(self):
        id_juego = self.sales_window.cmbGame.currentData()

        nombre_cli = self.sales_window.txtClient.text().strip()

        cantidad = self.sales_window.spnQty.value()

        id_empleado = self.manager.empleado_activo["id"]

        if not nombre_cli:
            QMessageBox.warning(
                self.sales_window,
                "Gamestore",
                "Escribe el nombre del cliente."
            )
            return

        if id_juego is None:
            QMessageBox.warning(
                self.sales_window,
                "Gamestore",
                "No hay juegos disponibles."
            )
            return

        partes = nombre_cli.split(" ", 1)

        nombre = partes[0]

        apellido = partes[1] if len(partes) > 1 else ""

        res_cli = self.manager.db.select(
            """
                SELECT id_cliente
                FROM clientes
                WHERE nombre = ?
                AND apellido = ?
            """,
            (nombre, apellido)
        )

        if res_cli:
            id_cliente = res_cli[0][0]

        else:
            email = f"{nombre.lower()}.{apellido.lower()}@gamestore.com"

            id_cliente = self.manager.db.insert(
                """
                    INSERT INTO clientes (
                        nombre,
                        apellido,
                        email
                    )
                    VALUES (?, ?, ?)
                """,
                (
                    nombre,
                    apellido,
                    email
                )
            )

        precio_res = self.manager.db.select(
            """
                SELECT precio
                FROM videojuegos
                WHERE id_juego = ?
            """,
            (id_juego,)
        )

        if not precio_res:
            return

        precio = float(precio_res[0][0])

        total = precio * cantidad

        id_venta = self.manager.db.insert(
            """
                INSERT INTO ventas (
                    id_cliente,
                    id_empleado,
                    total
                )
                VALUES (?, ?, ?)
            """,
            (
                id_cliente,
                id_empleado,
                total
            )
        )

        if id_venta:
            self.manager.db.insert(
                """
                    INSERT INTO detalle_ventas (
                        id_venta,
                        id_juego,
                        cantidad,
                        precio_unit
                    )
                    VALUES (?, ?, ?, ?)
                """,
                (
                    id_venta,
                    id_juego,
                    cantidad,
                    precio
                )
            )

            self.manager.db.update(
                """
                    UPDATE videojuegos
                    SET stock = stock - ?
                    WHERE id_juego = ?
                """,
                (
                    cantidad,
                    id_juego
                )
            )

            QMessageBox.information(
                self.sales_window,
                "Gamestore",
                f"Venta #{id_venta} registrada\n"
                f"Cliente: {nombre_cli}\n"
                f"Total: ${total:.2f}"
            )

            self.sales_window.txtClient.clear()

            self.sales_window.spnQty.setValue(1)

            self.cargar_juegos()

    def regresar_dashboard(self):
        self.sales_window.hide()
        self.window.show()