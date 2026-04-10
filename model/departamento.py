class Departamento:
    def __init__(self, nombre):
        self.nombre = nombre
        self.empleados = []

    def agregar_empleado(self, e):
        self.empleados.append(e)

    def listar_empleados(self):
        for e in self.empleados:
            e.mostrar_info()

    def eliminar_empleado(self, nombre):
        self.empleados = [e for e in self.empleados if e.nombre != nombre]
