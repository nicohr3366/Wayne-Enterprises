public class Empleado {
    private String nombre;
    private String cargo;
    private double salario;

    public Empleado(String nombre, String cargo, double salario) {
        this.nombre = nombre;
        this.cargo = cargo;
        this.salario = salario;
    }

    public String getNombre() {
        return nombre;
    }

    public String getCargo() {
        return cargo;
    }

    public double getSalario() {
        return salario;
    }

    public void mostrarInfo() {
        System.out.println("Nombre: " + nombre +
                           " | Cargo: " + cargo +
                           " | Salario: $" + salario);
    }
}
