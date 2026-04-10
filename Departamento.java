import java.util.ArrayList;

public class Departamento {
    private String nombre;
    private ArrayList<Empleado> empleados;

    public Departamento(String nombre) {
        this.nombre = nombre;
        empleados = new ArrayList<>();
    }

    public String getNombre() {
        return nombre;
    }

    public void agregarEmpleado(Empleado e) {
        empleados.add(e);
    }

    public void listarEmpleados() {
        if (empleados.isEmpty()) {
            System.out.println("No hay empleados.");
            return;
        }

        for (Empleado e : empleados) {
            e.mostrarInfo();
        }
    }

    public void eliminarEmpleado(String nombre) {
        empleados.removeIf(e -> e.getNombre().equalsIgnoreCase(nombre));
    }
}
