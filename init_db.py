import sqlite3

def crear_tablas():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # 1. Clientes (5 columnas)
    cursor.execute('CREATE TABLE IF NOT EXISTS clientes (cedula TEXT PRIMARY KEY, nombres TEXT, apellidos TEXT, direccion TEXT, telefono TEXT)')
    
    # 2. Medicamentos (4 columnas)
    cursor.execute('CREATE TABLE IF NOT EXISTS medicamentos (id_med INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, descripcion TEXT, dosis TEXT)')
    
    # 3. Mascotas (6 columnas: id, nombre, raza, edad, peso, cedula_cliente)
    cursor.execute('''CREATE TABLE IF NOT EXISTS mascotas (
        id_mascota TEXT PRIMARY KEY, nombre TEXT, raza TEXT, edad INTEGER, peso REAL, cedula_cliente TEXT,
        FOREIGN KEY(cedula_cliente) REFERENCES clientes(cedula))''')
    
    # 4. Tabla Intermedia: Tratamientos
    cursor.execute('''CREATE TABLE IF NOT EXISTS tratamientos (
        id_mascota TEXT, id_med INTEGER,
        FOREIGN KEY(id_mascota) REFERENCES mascotas(id_mascota),
        FOREIGN KEY(id_med) REFERENCES medicamentos(id_med))''')
    
    conn.commit()
    conn.close()

crear_tablas()