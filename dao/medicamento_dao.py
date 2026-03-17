import sqlite3
from models.medicamento import Medicamento

class MedicamentoDAO:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def crear(self, med):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = "INSERT INTO medicamentos (nombre, descripcion, dosis) VALUES (?, ?, ?)"
            cursor.execute(query, (med.nombre, med.descripcion, med.dosis))
            conn.commit()

    def obtener_por_id(self, id_med):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Ajusta el nombre de la tabla o columnas si en tu base de datos son distintos
            cursor.execute("SELECT id_med, nombre, descripcion, dosis FROM medicamentos WHERE id_med = ?", (id_med,))
            row = cursor.fetchone()
            if row:
                return Medicamento(row[0], row[1], row[2], row[3])
            return None

    def listar_todos(self):
        medicamentos = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM medicamentos")
            for row in cursor.fetchall():
                medicamentos.append(Medicamento(row[0], row[1], row[2], row[3]))
        return medicamentos
    
    def actualizar(self, med):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE medicamentos SET nombre=?, dosis=? WHERE id_med=?",
                           (med.nombre, med.dosis, med.id_med))
            conn.commit()

    def eliminar(self, id_med):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM medicamentos WHERE id_med=?", (id_med,))
            conn.commit()