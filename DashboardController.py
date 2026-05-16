class DashboardController:
    def __init__(self, window, manager):
        self.window = window
        self.manager = manager
        self.cargar_stats()

    def cargar_stats(self):
        db = self.manager.db

        total_juegos = db.select("SELECT COUNT(*) FROM videojuegos WHERE activo=1")
        total_ventas = db.select("SELECT COUNT(*) FROM ventas")
        total_clientes = db.select("SELECT COUNT(*) FROM clientes")

        try:
            self.window.lblGames.setText(f"Total videojuegos: {total_juegos[0][0]}")
        except:
            pass

        try:
            self.window.lblSales.setText(f"Ventas del día: {total_ventas[0][0]}")
        except:
            pass

        try:
            self.window.lblClients.setText(f"Clientes registrados: {total_clientes[0][0]}")
        except:
            pass