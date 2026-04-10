class Empresa:
    def __init__(self, nombre):
        self.nombre = nombre
        self.departamentos = []

    def agregar_departamento(self, d):
        self.departamentos.append(d)

    def buscar_departamento(self, nombre):
        for d in self.departamentos:
            if d.nombre == nombre:
                return d
        return None

    def listar_departamentos(self):
        for d in self.departamentos:
            print(d.nombre)

    def mostrar_todo(self):
        for d in self.departamentos:
            print("\n" + d.nombre)
            d.listar_empleados()
