"""
Pipeline completo de procesamiento de contratos
"""
import subprocess
import sys
import os


def run_step(name, command):
    """Ejecuta un paso del pipeline"""
    print(f"\n{'='*60}")
    print(f"Ejecutando: {name}")
    print(f"{'='*60}")

    result = subprocess.run(command, shell=True, capture_output=False)

    if result.returncode != 0:
        print(f"Error en: {name}")
        sys.exit(1)

    print(f"Completado: {name}")


def main():
    print("=" * 60)
    print("WAYNE DEFENSE - Pipeline ETL Completo")
    print("=" * 60)

    # Obtener ruta base
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(scripts_dir)

    steps = [
        ("Parsear XML de Contratos", "python xml_parser.py"),
        ("Transformar JSON de Licitaciones", "python json_transformer.py"),
        ("Generar Reporte HTML", "python generate_report.py")
    ]

    for name, command in steps:
        run_step(name, command)

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    print("\nArchivos generados:")
    print("   - data/processed/contratos_parseados.json")
    print("   - data/processed/licitaciones_transformadas.json")
    print("   - output/dashboard.html")
    print("\nAbre output/dashboard.html en tu navegador")


if __name__ == "__main__":
    main()
