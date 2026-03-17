import sqlite3
from models.cliente import Cliente

class ClienteDAO:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def crear(self, cliente):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                query = "INSERT INTO clientes (cedula, nombres, apellidos, direccion, telefono) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(query, (cliente.cedula, cliente.nombres, cliente.apellidos, cliente.direccion, cliente.telefono))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False # Cédula duplicada
        
    def obtener_por_id(self, cedula):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cedula, nombres, apellidos, direccion, telefono FROM clientes WHERE cedula = ?", (cedula,))
            row = cursor.fetchone()
            if row:
                # Retornamos el objeto Cliente con los datos encontrados
                return Cliente(row[0], row[1], row[2], row[3], row[4])
            return None

    def listar_todos(self):
        clientes = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            for row in cursor.fetchall():
                clientes.append(Cliente(row[0], row[1], row[2], row[3], row[4]))
        return clientes
    
    def actualizar(self, cliente):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE clientes SET nombres=?, apellidos=?, telefono=? WHERE cedula=?",
                           (cliente.nombres, cliente.apellidos, cliente.telefono, cliente.cedula))
            conn.commit()

    def eliminar(self, cedula):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE cedula = ?", (cedula,))
            conn.commit()