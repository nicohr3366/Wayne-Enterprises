from model.empresa import Empresa
from model.departamento import Departamento
from model.empleado import Empleado

def main():
    empresa = Empresa("Wayne Industries")

    while True:
        print("\n=== WAYNE INDUSTRIES ===")
        print("1. Crear departamento")
        print("2. Agregar empleado")
        print("3. Listar departamentos")
        print("4. Ver empleados por departamento")
        print("5. Eliminar empleado")
        print("6. Mostrar toda la empresa")
        print("0. Salir")

        opcion = input("Opción: ")

        if opcion == "1":
            nombre = input("Nombre del departamento: ")
            empresa.agregar_departamento(Departamento(nombre))

        elif opcion == "2":
            dep = empresa.buscar_departamento(input("Departamento: "))
            if dep:
                nombre = input("Nombre: ")
                cargo = input("Cargo: ")
                salario = float(input("Salario: "))
                dep.agregar_empleado(Empleado(nombre, cargo, salario))
            else:
                print("No existe")

        elif opcion == "3":
            empresa.listar_departamentos()

        elif opcion == "4":
            dep = empresa.buscar_departamento(input("Departamento: "))
            if dep:
                dep.listar_empleados()

        elif opcion == "5":
            dep = empresa.buscar_departamento(input("Departamento: "))
            if dep:
                dep.eliminar_empleado(input("Empleado: "))

        elif opcion == "6":
            empresa.mostrar_todo()

        elif opcion == "0":
            break

if __name__ == "__main__":
    main()
