class Empleado:
    def __init__(self, nombre, cargo, salario):
        self.nombre = nombre
        self.cargo = cargo
        self.salario = salario

    def mostrar_info(self):
        print(f"{self.nombre} - {self.cargo} - ${self.salario}")
