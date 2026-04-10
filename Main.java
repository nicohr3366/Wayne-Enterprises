import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        Empresa empresa = new Empresa("Wayne Industries");

        int opcion;

        do {
            System.out.println("\n=== WAYNE INDUSTRIES ===");
            System.out.println("1. Crear departamento");
            System.out.println("2. Agregar empleado");
            System.out.println("3. Listar departamentos");
            System.out.println("4. Ver empleados por departamento");
            System.out.println("5. Eliminar empleado");
            System.out.println("6. Mostrar toda la empresa");
            System.out.println("0. Salir");
            System.out.print("Opción: ");
            opcion = sc.nextInt();
            sc.nextLine();

            switch (opcion) {

                case 1:
                    System.out.print("Nombre del departamento: ");
                    String nombreDep = sc.nextLine();
                    empresa.agregarDepartamento(new Departamento(nombreDep));
                    System.out.println("Departamento creado.");
                    break;

                case 2:
                    System.out.print("Departamento: ");
                    String depNombre = sc.nextLine();
                    Departamento dep = empresa.buscarDepartamento(depNombre);

                    if (dep != null) {
                        System.out.print("Nombre empleado: ");
                        String nombre = sc.nextLine();

                        System.out.print("Cargo: ");
                        String cargo = sc.nextLine();

                        System.out.print("Salario: ");
                        double salario = sc.nextDouble();
                        sc.nextLine();

                        dep.agregarEmpleado(new Empleado(nombre, cargo, salario));
                        System.out.println("Empleado agregado.");
                    } else {
                        System.out.println("Departamento no existe.");
                    }
                    break;

                case 3:
                    empresa.listarDepartamentos();
                    break;

                case 4:
                    System.out.print("Departamento: ");
                    String buscar = sc.nextLine();
                    Departamento d = empresa.buscarDepartamento(buscar);

                    if (d != null) {
                        d.listarEmpleados();
                    } else {
                        System.out.println("No existe.");
                    }
                    break;

                case 5:
                    System.out.print("Departamento: ");
                    String depEliminar = sc.nextLine();
                    Departamento d2 = empresa.buscarDepartamento(depEliminar);

                    if (d2 != null) {
                        System.out.print("Nombre empleado a eliminar: ");
                        String nombreEliminar = sc.nextLine();
                        d2.eliminarEmpleado(nombreEliminar);
                        System.out.println("Empleado eliminado.");
                    } else {
                        System.out.println("Departamento no existe.");
                    }
                    break;

                case 6:
                    empresa.mostrarTodo();
                    break;

                case 0:
                    System.out.println("Saliendo...");
                    break;

                default:
                    System.out.println("Opción inválida.");
            }

        } while (opcion != 0);

        sc.close();
    }
}
