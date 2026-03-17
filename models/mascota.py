class Mascota:
    def __init__(self, id_mascota, nombre, raza, edad, peso, medicamento, cliente):
        self.id_mascota = id_mascota
        self.nombre = nombre
        self.raza = raza
        self.edad = edad
        self.peso = peso
        self.medicamento = medicamento # Relación con Medicamento
        self.cliente = cliente         # Relación con Cliente (Cédula)