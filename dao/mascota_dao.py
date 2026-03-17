import sqlite3

class MascotaDAO:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def listar_con_detalles(self):
        """Reporte con: ID, Nombre, Raza, Edad, Peso, Dueño y Medicamentos"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT m.id_mascota, m.nombre, m.raza, m.edad, m.peso, 
                       c.nombres || ' ' || c.apellidos as dueño,
                       (SELECT GROUP_CONCAT(med.nombre, ', ') 
                        FROM tratamientos t 
                        JOIN medicamentos med ON t.id_med = med.id_med 
                        WHERE t.id_mascota = m.id_mascota) as lista_meds
                FROM mascotas m
                JOIN clientes c ON m.cedula_cliente = c.cedula
            """
            cursor.execute(query)
            return cursor.fetchall()

    def obtener_por_id(self, id_mascota):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mascotas WHERE id_mascota = ?", (id_mascota,))
            return cursor.fetchone()

    def obtener_ids_medicamentos(self, id_mascota):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_med FROM tratamientos WHERE id_mascota = ?", (id_mascota,))
            return [fila[0] for fila in cursor.fetchall()]

    def crear(self, mascota, lista_ids_meds):
        """Solución al error de 7 columnas indicando campos específicos"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO mascotas (id_mascota, nombre, raza, edad, peso, cedula_cliente) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (mascota.id_mascota, mascota.nombre, mascota.raza, 
                  mascota.edad, mascota.peso, mascota.cliente))
            
            for id_med in lista_ids_meds:
                cursor.execute("INSERT INTO tratamientos (id_mascota, id_med) VALUES (?, ?)", 
                               (mascota.id_mascota, id_med))
            conn.commit()

    def actualizar_completo(self, mascota, lista_ids_meds):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE mascotas 
                SET nombre=?, raza=?, edad=?, peso=?, cedula_cliente=? 
                WHERE id_mascota=?
            """, (mascota.nombre, mascota.raza, mascota.edad, 
                  mascota.peso, mascota.cliente, mascota.id_mascota))
            
            cursor.execute("DELETE FROM tratamientos WHERE id_mascota = ?", (mascota.id_mascota,))
            for id_med in lista_ids_meds:
                cursor.execute("INSERT INTO tratamientos (id_mascota, id_med) VALUES (?, ?)", 
                               (mascota.id_mascota, id_med))
            conn.commit()