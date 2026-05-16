import mariadb


class Connection:
    def __init__(self):
        self.config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "gamestore_db",
            "port": 3306,
        }

        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mariadb.connect(**self.config)
            self.cursor = self.connection.cursor()
            print("Conexión exitosa a gamestore_db ✓")

        except mariadb.Error as e:
            print(f"Error de conexión: {e}")

    def select(self, sql, values=()):
        try:
            self.cursor.execute(sql, values)
            return self.cursor.fetchall()

        except mariadb.Error as e:
            print(f"Error SELECT: {e}")
            return []

    def insert(self, sql, values):
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()

            return self.cursor.lastrowid

        except mariadb.Error as e:
            print(f"Error INSERT: {e}")
            self.connection.rollback()
            return None

    def update(self, sql, values):
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()

            return self.cursor.rowcount

        except mariadb.Error as e:
            print(f"Error UPDATE: {e}")
            self.connection.rollback()
            return 0

    def delete(self, sql, values):
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()

            return self.cursor.rowcount

        except mariadb.Error as e:
            print(f"Error DELETE: {e}")
            self.connection.rollback()
            return 0

    def close(self):
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()