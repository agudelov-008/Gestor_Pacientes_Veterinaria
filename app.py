# --- PARCHE DE COMPATIBILIDAD PARA PYTHON 3.10+ ---
import collections
if not hasattr(collections, 'MutableMapping'):
    import collections.abc
    collections.MutableMapping = collections.abc.MutableMapping
# --------------------------------------------------

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 
from dao.cliente_dao import ClienteDAO
from dao.medicamento_dao import MedicamentoDAO
from dao.mascota_dao import MascotaDAO
from models.cliente import Cliente
from models.medicamento import Medicamento
from models.mascota import Mascota
from flask_graphql import GraphQLView
from esquema_graphql import schema  

app = Flask(__name__)
app.secret_key = "pets_secret_key"

db_path = 'database.db'
cliente_dao = ClienteDAO(db_path)
med_dao = MedicamentoDAO(db_path)
mascota_dao = MascotaDAO(db_path)

# --- RUTAS PRINCIPALES ---

@app.route('/')
def index():
    mascotas_detalles = mascota_dao.listar_con_detalles()
    return render_template('index.html', mascotas=mascotas_detalles)

# --- CRUD CLIENTES ---

@app.route('/clientes', methods=['GET', 'POST'])
def gestionar_clientes():
    if request.method == 'POST':
        c = Cliente(
            request.form.get('cedula'), 
            request.form.get('nombres'),
            request.form.get('apellidos'), 
            request.form.get('direccion'),
            request.form.get('telefono')
        )
        
        # Como el DAO devuelve True o False, usamos un IF
        fue_exitoso = cliente_dao.crear(c)
        
        if fue_exitoso:
            flash("Cliente registrado con éxito", "success")
        else:
            flash("Error: Ya existe un cliente registrado con esta Cédula.", "danger")
            
        return redirect(url_for('gestionar_clientes'))
    
    lista_db = cliente_dao.listar_todos()
    return render_template('clientes.html', clientes=lista_db)

@app.route('/clientes/editar/<cedula>', methods=['GET', 'POST'])
def editar_cliente(cedula):
    if request.method == 'POST':
        c = Cliente(
            cedula, request.form.get('nombres'), request.form.get('apellidos'),
            request.form.get('direccion'), request.form.get('telefono')
        )
        cliente_dao.actualizar(c)
        flash("Cambios guardados", "success")
        return redirect(url_for('gestionar_clientes'))
    
    c_datos = cliente_dao.obtener_por_id(cedula)
    return render_template('editar_cliente.html', c=c_datos)

@app.route('/clientes/eliminar/<cedula>')
def eliminar_cliente(cedula):
    cliente_dao.eliminar(cedula)
    flash("Cliente eliminado del sistema", "warning")
    return redirect(url_for('gestionar_clientes'))

# --- CRUD MEDICAMENTOS ---

@app.route('/medicamentos', methods=['GET', 'POST'])
def gestionar_medicamentos():
    if request.method == 'POST':
        m = Medicamento(
            None, request.form.get('nombre'), 
            request.form.get('descripcion'), request.form.get('dosis')
        )
        try:
            med_dao.crear(m)
            flash("Medicamento añadido", "success")
        except Exception as e:
            flash("Error al registrar el medicamento en la base de datos.", "danger")
            
        return redirect(url_for('gestionar_medicamentos'))
    
    lista_m = med_dao.listar_todos()
    return render_template('medicamentos.html', medicamentos=lista_m)

@app.route('/medicamentos/editar/<int:id_med>', methods=['GET', 'POST'])
def editar_medicamento(id_med):
    if request.method == 'POST':
        m = Medicamento(
            id_med, request.form.get('nombre'), 
            request.form.get('descripcion'), request.form.get('dosis')
        )
        med_dao.actualizar(m)
        flash("Medicamento actualizado", "success")
        return redirect(url_for('gestionar_medicamentos'))
    
    m_datos = med_dao.obtener_por_id(id_med)
    return render_template('editar_medicamento.html', m=m_datos)

@app.route('/medicamentos/eliminar/<int:id_med>')
def eliminar_medicamento(id_med):
    med_dao.eliminar(id_med)
    flash("Medicamento eliminado", "danger")
    return redirect(url_for('gestionar_medicamentos'))

# --- RUTAS DE MASCOTAS ---

@app.route('/mascotas', methods=['GET', 'POST'])
def gestionar_mascotas():
    if request.method == 'POST':
        ids_meds = request.form.getlist('medicamentos_seleccionados')
        m = Mascota(
            request.form['id_mascota'], request.form['nombre'],
            request.form['raza'], request.form['edad'],
            request.form['peso'], None, 
            request.form['cedula_cliente']
        )
        
        # Manejo de Excepciones para Mascotas (El error que te salió antes)
        try:
            mascota_dao.crear(m, ids_meds)
            flash("Mascota registrada con tratamiento completo", "success")
        except sqlite3.IntegrityError:
            flash("Error: Ya existe un paciente registrado con ese ID.", "danger")
        except Exception as e:
            flash(f"Ocurrió un error al guardar la mascota: {str(e)}", "danger")
            
        return redirect(url_for('index'))
    
    return render_template('form_mascota.html', 
                           clientes=cliente_dao.listar_todos(),
                           medicamentos=med_dao.listar_todos())

@app.route('/mascota/detalle/<id_mascota>', methods=['GET', 'POST'])
def detalle_mascota(id_mascota):
    if request.method == 'POST':
        ids_meds = [int(x) for x in request.form.getlist('medicamentos_seleccionados')]
        m = Mascota(
            id_mascota, request.form.get('nombre'), request.form.get('raza'),
            request.form.get('edad'), request.form.get('peso'), 
            None, request.form.get('cedula_cliente')
        )
        mascota_dao.actualizar_completo(m, ids_meds)
        flash("Expediente actualizado correctamente", "success")
        return redirect(url_for('index'))
    
    datos_m = mascota_dao.obtener_por_id(id_mascota)
    meds_db = mascota_dao.obtener_ids_medicamentos(id_mascota)
    meds_actuales = [str(x) for x in meds_db]
    
    return render_template('detalle_mascota.html', 
                           m=datos_m, meds_actuales=meds_actuales,
                           clientes=cliente_dao.listar_todos(),
                           medicamentos=med_dao.listar_todos())

# --- RUTA GRAPHQL ---
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # ¡Esto activa la interfaz visual de pruebas!
    )
)

if __name__ == '__main__':
    app.run(debug=True)