import graphene
from dao.cliente_dao import ClienteDAO
from models.cliente import Cliente

# Instanciamos el DAO para conectarnos a la BD
cliente_dao = ClienteDAO('database.db')

# 1. SCHEMA: 
class ClienteType(graphene.ObjectType):
    cedula = graphene.String()
    nombres = graphene.String()
    apellidos = graphene.String()
    direccion = graphene.String()
    telefono = graphene.String()

# 2. QUERIES & RESOLVERS 
class Query(graphene.ObjectType):
    # Definimos la consulta 'clientes' que devuelve una lista
    clientes = graphene.List(ClienteType)
    # Definimos la consulta 'cliente' que busca por cédula
    cliente = graphene.Field(ClienteType, cedula=graphene.String(required=True))

    # Resolver para listar todos
    def resolve_clientes(self, info):
        # El DAO devuelve una lista de objetos Cliente
        clientes_db = cliente_dao.listar_todos()
        # Convertimos los objetos al tipo GraphQL usando el punto (.)
        return [
            ClienteType(
                cedula=c.cedula, 
                nombres=c.nombres, 
                apellidos=c.apellidos, 
                direccion=c.direccion, 
                telefono=c.telefono
            ) for c in clientes_db
        ]

    # Resolver para buscar uno solo
    def resolve_cliente(self, info, cedula):
        c = cliente_dao.obtener_por_id(cedula) # Devuelve un objeto Cliente
        if c:
            return ClienteType(cedula=c.cedula, nombres=c.nombres, apellidos=c.apellidos, direccion=c.direccion, telefono=c.telefono)
        return None

# 3. MUTATIONS & RESOLVERS (Para modificar datos / CRUD)
class CrearCliente(graphene.Mutation):
    # Argumentos que recibe la mutación
    class Arguments:
        cedula = graphene.String(required=True)
        nombres = graphene.String(required=True)
        apellidos = graphene.String(required=True)
        direccion = graphene.String(required=True)
        telefono = graphene.String(required=True)

    # Lo que devuelve la mutación (Si fue exitoso y el cliente creado)
    ok = graphene.Boolean()
    cliente = graphene.Field(ClienteType)

    # Resolver de la mutación de CREAR (La acción real)
    def mutate(self, info, cedula, nombres, apellidos, direccion, telefono):
        nuevo_cliente = Cliente(cedula, nombres, apellidos, direccion, telefono)
        try:
            cliente_dao.crear(nuevo_cliente)
            c_gql = ClienteType(cedula=cedula, nombres=nombres, apellidos=apellidos, direccion=direccion, telefono=telefono)
            return CrearCliente(ok=True, cliente=c_gql)
        except Exception:
            # Falla si la cédula está duplicada, por ejemplo
            return CrearCliente(ok=False, cliente=None)


class ActualizarCliente(graphene.Mutation):
    class Arguments:
        # La cédula es obligatoria para saber a quién editar
        cedula = graphene.String(required=True)
        nombres = graphene.String()
        apellidos = graphene.String()
        direccion = graphene.String()
        telefono = graphene.String()

    ok = graphene.Boolean()
    cliente = graphene.Field(ClienteType)

    # Resolver de la mutación de ACTUALIZAR
    def mutate(self, info, cedula, nombres=None, apellidos=None, direccion=None, telefono=None):
        # 1. Buscamos el cliente actual para no perder datos si no se envían todos
        cliente_existente = cliente_dao.obtener_por_id(cedula)
        
        if not cliente_existente:
            return ActualizarCliente(ok=False, cliente=None)

        # 2. Actualizamos solo los campos que vengan en la petición (si no, dejamos el original)
        c_modificado = Cliente(
            cedula,
            nombres if nombres else cliente_existente.nombres,
            apellidos if apellidos else cliente_existente.apellidos,
            direccion if direccion else cliente_existente.direccion,
            telefono if telefono else cliente_existente.telefono
        )

        try:
            cliente_dao.actualizar(c_modificado)
            # Convertimos a ClienteType para la respuesta de GraphQL
            c_gql = ClienteType(
                cedula=c_modificado.cedula,
                nombres=c_modificado.nombres,
                apellidos=c_modificado.apellidos,
                direccion=c_modificado.direccion,
                telefono=c_modificado.telefono
            )
            return ActualizarCliente(ok=True, cliente=c_gql)
        except Exception:
            return ActualizarCliente(ok=False, cliente=None)


# Agrupamos las mutaciones
class Mutation(graphene.ObjectType):
    crear_cliente = CrearCliente.Field()
    actualizar_cliente = ActualizarCliente.Field()

# 4. EXPORTAMOS EL ESQUEMA COMPLETO
schema = graphene.Schema(query=Query, mutation=Mutation)