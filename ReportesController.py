from PyQt6 import uic
from PyQt6.QtWidgets import QTableWidgetItem


class reportes:
    def __init__(self, window, manager):
        self.window = window
        self.manager = manager

        self.reports_window = None

        self.window.btnReports.clicked.connect(
            self.handle_reportes
        )

    def handle_reportes(self):
        if self.reports_window is None:
            self.reports_window = uic.loadUi(
                "./views/5reportes.ui"
            )

            self.reports_window.btnAdd.clicked.connect(
                self.regresar_dashboard
            )

            self.reports_window.btnGenerate.clicked.connect(
                self.reporte_ventas
            )

            self.reports_window.btnPrint.clicked.connect(
                self.reporte_inventario
            )

        self.reporte_ventas()

        self.window.hide()
        self.reports_window.show()

    def reporte_ventas(self):
        sql = """
            SELECT
                v.id_venta,

                vj.titulo AS juego,

                CONCAT(
                    c.nombre,
                    ' ',
                    c.apellido
                ) AS cliente,

                dv.cantidad,

                CONCAT(
                    '$',
                    FORMAT(v.total, 2)
                ) AS total

            FROM ventas v

            JOIN clientes c
                ON c.id_cliente = v.id_cliente

            JOIN detalle_ventas dv
                ON dv.id_venta = v.id_venta

            JOIN videojuegos vj
                ON vj.id_juego = dv.id_juego

            ORDER BY v.fecha_venta DESC
        """

        filas = self.manager.db.select(sql)

        headers = [
            "# Venta",
            "Juego",
            "Cliente",
            "Cantidad",
            "Total"
        ]

        self._llenar_tabla(
            filas,
            headers
        )

    def reporte_inventario(self):
        sql = """
            SELECT
                vj.titulo,
                vj.plataforma,
                vj.precio,
                vj.stock,

                COUNT(dv.id_detalle) AS veces_vendido

            FROM videojuegos vj

            LEFT JOIN detalle_ventas dv
                ON dv.id_juego = vj.id_juego

            WHERE vj.activo = 1

            GROUP BY vj.id_juego

            ORDER BY veces_vendido DESC
        """

        filas = self.manager.db.select(sql)

        headers = [
            "Título",
            "Plataforma",
            "Precio",
            "Stock",
            "Veces vendido"
        ]

        self._llenar_tabla(
            filas,
            headers
        )

    def _llenar_tabla(self, filas, headers):
        tabla = self.reports_window.tblReport

        tabla.setColumnCount(len(headers))
        tabla.setHorizontalHeaderLabels(headers)

        tabla.setRowCount(len(filas))

        for row_idx, fila in enumerate(filas):
            for col_idx, valor in enumerate(fila):
                tabla.setItem(
                    row_idx,
                    col_idx,
                    QTableWidgetItem(str(valor))
                )

    def regresar_dashboard(self):
        self.reports_window.hide()
        self.window.show()