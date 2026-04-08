# PETS S.A. - Sistema de Gestión Veterinaria 🐾

Una aplicación web desarrollada con **Flask** para la gestión integral de una clínica veterinaria. El sistema permite administrar clientes, medicamentos y los expedientes médicos de las mascotas utilizando el patrón de diseño DAO (Data Access Object) para una arquitectura limpia y escalable.

## 🚀 Características Principales

* **Gestión de Clientes:** CRUD completo (Crear, Leer, Actualizar, Eliminar) de dueños de mascotas.
* **Catálogo de Medicamentos:** Registro y control de fármacos y dosis.
* **Expedientes de Mascotas:** Vinculación de mascotas con sus dueños y asignación de múltiples tratamientos médicos en un solo reporte.
* **Arquitectura DAO:** Separación clara entre la lógica de negocio y el acceso a la base de datos.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3, Flask
* **Base de Datos:** SQLite3
* **Frontend:** HTML5, Bootstrap 5, Jinja2

## ⚙️ Instalación y Uso

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/nombre-del-repo.git](https://github.com/tu-usuario/nombre-del-repo.git)

2. Crear y activar el entorno virtual:
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate

3. Instalar dependencias
    pip install -r requirements.txt

4. Ejecutar la apicación
    python app.py