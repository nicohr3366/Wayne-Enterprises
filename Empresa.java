import java.util.ArrayList;

public class Empresa {
    private String nombre;
    private ArrayList<Departamento> departamentos;

    public Empresa(String nombre) {
        this.nombre = nombre;
        departamentos = new ArrayList<>();
    }

    public void agregarDepartamento(Departamento d) {
        departamentos.add(d);
    }

    public Departamento buscarDepartamento(String nombre) {
        for (Departamento d : departamentos) {
            if (d.getNombre().equalsIgnoreCase(nombre)) {
                return d;
            }
        }
        return null;
    }

    public void listarDepartamentos() {
        if (departamentos.isEmpty()) {
            System.out.println("No hay departamentos.");
            return;
        }

        for (Departamento d : departamentos) {
            System.out.println("- " + d.getNombre());
        }
    }

    public void mostrarTodo() {
        for (Departamento d : departamentos) {
            System.out.println("\nDepartamento: " + d.getNombre());
            d.listarEmpleados();
        }
    }
}
