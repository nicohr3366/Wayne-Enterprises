# Guía Individual: Pérez - Dataset #11

> **Responsable:** Pérez  
> **ID:** #11  
> **Dataset:** Recursos Humanos (Wayne Manor)  
> **Descripción:** Personal de servicio y seguridad privada. Gestión de roles y permisos (RBAC).  
> **Rama Git:** `perez`  

---

## ¿Qué es tu Dataset?

Tu trabajo es crear un **sistema de gestión de Recursos Humanos** para Wayne Manor que procese:

- **Personal de servicio** (limpieza, cocina, mantenimiento)
- **Seguridad privada** (guardias, escoltas)
- **Sistema de roles y permisos** (RBAC)
- **Nómina y turnos** de empleados

**Ejemplo real:** Como un ERP de RRHH que gestiona quién trabaja dónde y con qué permisos.

---

## Paso a Paso: Crear tu Sistema RRHH

### Paso 1: Crear Estructura

```bash
# Estás en Wayne-Enterprises/
mkdir -p perez_rrhh/{data,scripts,reports}
cd perez_rrhh

touch data/__init__.py
touch scripts/__init__.py
```

Estructura:
```
perez_rrhh/
├── data/
│   ├── empleados.csv          # Base de empleados
│   ├── turnos.csv             # Horarios de trabajo
│   └── permisos.json          # Sistema RBAC
├── scripts/
│   ├── hr_manager.py          # Gestión de empleados
│   ├── rbac_system.py         # Control de permisos
│   └── nomina.py              # Cálculo de nómina
└── reports/
    └── reporte_rrhh.html      # Reporte final
```

---

### Paso 2: Datos de Empleados

**`data/empleados.csv`:**

```csv
id,nombre,apellido,rol,departamento,fecha_ingreso,salario_mensual,activo,supervisor
EMP001,Alfred,Pennyworth,Jefe de Servicio,Administracion,1985-03-15,8000,si,Bruce Wayne
EMP002,Lucius,Fox,Asistente Ejecutivo,Tecnologia,1990-07-20,9500,si,Bruce Wayne
EMP003,Martha,Keen,Cocinera Principal,Servicios,2005-01-10,3500,si,Alfred Pennyworth
EMP004,James,Corbett,Jardinero,Servicios,2008-04-22,2800,si,Alfred Pennyworth
EMP005,Sarah,Vance,Enfermera,Salud,2012-09-05,4200,si,Alfred Pennyworth
EMP006,Michael,Stone,Guardia de Seguridad,Seguridad,2015-11-18,3200,si,Security Chief
EMP007,Rachel,Dawes,Abogada Corporativa,Legal,2010-06-30,7800,si,Bruce Wayne
EMP008,Harvey,Bullock,Supervisor Seguridad,Seguridad,2000-02-14,5500,si,Bruce Wayne
EMP009,Tim,Drake,Interno Tecnologia,Tecnologia,2023-08-01,2500,si,Lucius Fox
EMP010,Barbara,Gordon,Analista Sistemas,Tecnologia,2018-05-20,5800,si,Lucius Fox
```

**`data/turnos.csv`:**

```csv
empleado_id,dia_semana,hora_inicio,hora_fin,area
EMP001,Lunes,06:00,14:00,Wayne Manor
EMP001,Martes,06:00,14:00,Wayne Manor
EMP003,Lunes,05:00,13:00,Cocina
EMP003,Martes,05:00,13:00,Cocina
EMP006,Lunes,22:00,06:00,Perimetro
EMP006,Martes,22:00,06:00,Perimetro
EMP008,Miercoles,08:00,18:00,Comando
EMP009,Lunes,09:00,17:00,Oficina Tech
```

---

### Paso 3: Sistema RBAC (Roles y Permisos)

**`data/permisos.json`:**

```json
{
  "roles": [
    {
      "nombre": "administrador",
      "nivel": 1,
      "permisos": [
        "ver_todo",
        "editar_empleados",
        "eliminar_empleados",
        "gestionar_nomina",
        "ver_reportes_admin",
        "acceder_baticueva"
      ],
      "descripcion": "Acceso total al sistema"
    },
    {
      "nombre": "supervisor",
      "nivel": 2,
      "permisos": [
        "ver_equipo",
        "editar_turnos",
        "aprobar_vacaciones",
        "ver_reportes_depto"
      ],
      "descripcion": "Gestión de departamento"
    },
    {
      "nombre": "empleado",
      "nivel": 3,
      "permisos": [
        "ver_perfil",
        "solicitar_vacaciones",
        "ver_turnos"
      ],
      "descripcion": "Acceso básico"
    },
    {
      "nombre": "seguridad",
      "nivel": 2,
      "permisos": [
        "acceder_perimetro",
        "ver_camaras",
        "control_acceso",
        "ver_empleados_activos"
      ],
      "descripcion": "Personal de seguridad"
    }
  ],
  "asignaciones": [
    {"empleado_id": "EMP001", "rol": "administrador"},
    {"empleado_id": "EMP002", "rol": "administrador"},
    {"empleado_id": "EMP003", "rol": "empleado"},
    {"empleado_id": "EMP004", "rol": "empleado"},
    {"empleado_id": "EMP005", "rol": "supervisor"},
    {"empleado_id": "EMP006", "rol": "seguridad"},
    {"empleado_id": "EMP007", "rol": "supervisor"},
    {"empleado_id": "EMP008", "rol": "seguridad"},
    {"empleado_id": "EMP009", "rol": "empleado"},
    {"empleado_id": "EMP010", "rol": "supervisor"}
  ]
}
```

---

### Paso 4: Script de Gestión RRHH

**`scripts/hr_manager.py`:**

```python
"""
Sistema de Gestión de Recursos Humanos - Wayne Manor
"""
import csv
import json
from datetime import datetime, timedelta


def load_empleados(filepath='data/empleados.csv'):
    """Carga base de empleados"""
    empleados = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            empleados.append({
                'id': row['id'],
                'nombre': f"{row['nombre']} {row['apellido']}",
                'rol': row['rol'],
                'departamento': row['departamento'],
                'fecha_ingreso': row['fecha_ingreso'],
                'salario_mensual': float(row['salario_mensual']),
                'activo': row['activo'] == 'si',
                'supervisor': row['supervisor']
            })
    return empleados


def load_turnos(filepath='data/turnos.csv'):
    """Carga turnos de empleados"""
    turnos = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            turnos.append({
                'empleado_id': row['empleado_id'],
                'dia': row['dia_semana'],
                'hora_inicio': row['hora_inicio'],
                'hora_fin': row['hora_fin'],
                'area': row['area']
            })
    return turnos


def buscar_empleado(empleados, emp_id):
    """Busca empleado por ID"""
    for emp in empleados:
        if emp['id'] == emp_id:
            return emp
    return None


def empleados_por_departamento(empleados, depto):
    """Filtra empleados por departamento"""
    return [e for e in empleados if e['departamento'] == depto]


def calcular_antiguedad(fecha_ingreso):
    """Calcula años de antigüedad"""
    fecha = datetime.strptime(fecha_ingreso, '%Y-%m-%d')
    hoy = datetime.now()
    return (hoy - fecha).days // 365


def calcular_bonificacion(empleado):
    """Calcula bonificación por antigüedad"""
    antiguedad = calcular_antiguedad(empleado['fecha_ingreso'])
    salario = empleado['salario_mensual']
    
    if antiguedad >= 20:
        return salario * 0.20  # 20% de bonificación
    elif antiguedad >= 10:
        return salario * 0.10  # 10% de bonificación
    elif antiguedad >= 5:
        return salario * 0.05   # 5% de bonificación
    return 0


def generar_reporte_empleados(empleados):
    """Genera estadísticas de empleados"""
    reporte = {
        'total_empleados': len(empleados),
        'activos': len([e for e in empleados if e['activo']]),
        'por_departamento': {},
        'promedio_salario': sum(e['salario_mensual'] for e in empleados) / len(empleados),
        'costo_total_nomina': sum(e['salario_mensual'] for e in empleados),
        'mas_antiguos': []
    }
    
    # Contar por departamento
    for emp in empleados:
        depto = emp['departamento']
        if depto not in reporte['por_departamento']:
            reporte['por_departamento'][depto] = []
        reporte['por_departamento'][depto].append(emp['nombre'])
    
    # Top 3 más antiguos
    empleados_sorted = sorted(empleados, 
                             key=lambda x: calcular_antiguedad(x['fecha_ingreso']), 
                             reverse=True)
    reporte['mas_antiguos'] = [
        {
            'nombre': e['nombre'],
            'antiguedad': calcular_antiguedad(e['fecha_ingreso'])
        }
        for e in empleados_sorted[:3]
    ]
    
    return reporte


def mostrar_turnos_empleado(turnos, empleado_id):
    """Muestra turnos de un empleado"""
    turnos_emp = [t for t in turnos if t['empleado_id'] == empleado_id]
    return turnos_emp


if __name__ == "__main__":
    # Cargar datos
    empleados = load_empleados()
    turnos = load_turnos()
    
    print("=" * 60)
    print("🏛️ WAYNE MANOR - Sistema de RRHH")
    print("=" * 60)
    
    # Reporte general
    reporte = generar_reporte_empleados(empleados)
    
    print(f"\n📊 Resumen:")
    print(f"   Total empleados: {reporte['total_empleados']}")
    print(f"   Empleados activos: {reporte['activos']}")
    print(f"   Promedio salario: ${reporte['promedio_salario']:,.2f}")
    print(f"   Costo mensual total: ${reporte['costo_total_nomina']:,.2f}")
    
    print(f"\n🏢 Por departamento:")
    for depto, nombres in reporte['por_departamento'].items():
        print(f"   {depto}: {len(nombres)} empleados")
    
    print(f"\n🏆 Empleados más antiguos:")
    for emp in reporte['mas_antiguos']:
        print(f"   {emp['nombre']}: {emp['antiguedad']} años")
    
    # Ejemplo de búsqueda
    emp = buscar_empleado(empleados, 'EMP001')
    if emp:
        bonif = calcular_bonificacion(emp)
        print(f"\n💰 Empleado destacado:")
        print(f"   {emp['nombre']} - {emp['rol']}")
        print(f"   Salario: ${emp['salario_mensual']:,.2f}")
        print(f"   Bonificación: ${bonif:,.2f}")
```

---

### Paso 5: Sistema RBAC

**`scripts/rbac_system.py`:**

```python
"""
Sistema RBAC (Role-Based Access Control)
Gestión de permisos y roles
"""
import json


def load_rbac_config(filepath='data/permisos.json'):
    """Carga configuración de roles y permisos"""
    with open(filepath, 'r') as file:
        return json.load(file)


def get_empleado_rol(empleado_id, asignaciones):
    """Obtiene el rol de un empleado"""
    for asig in asignaciones:
        if asig['empleado_id'] == empleado_id:
            return asig['rol']
    return None


def get_role_permissions(rol_nombre, roles):
    """Obtiene permisos de un rol"""
    for rol in roles:
        if rol['nombre'] == rol_nombre:
            return rol['permisos']
    return []


def check_permission(empleado_id, permiso_requerido, rbac_config):
    """
    Verifica si un empleado tiene un permiso específico
    Retorna: (tiene_permiso, rol, nivel)
    """
    roles = rbac_config['roles']
    asignaciones = rbac_config['asignaciones']
    
    # Obtener rol del empleado
    rol_nombre = get_empleado_rol(empleado_id, asignaciones)
    if not rol_nombre:
        return False, None, None
    
    # Buscar permisos del rol
    for rol in roles:
        if rol['nombre'] == rol_nombre:
            tiene_permiso = permiso_requerido in rol['permisos']
            return tiene_permiso, rol_nombre, rol['nivel']
    
    return False, rol_nombre, None


def get_empleados_con_permiso(permiso, rbac_config, empleados):
    """Obtiene todos los empleados que tienen un permiso específico"""
    empleados_con_permiso = []
    
    for asig in rbac_config['asignaciones']:
        emp_id = asig['empleado_id']
        tiene_perm, rol, nivel = check_permission(emp_id, permiso, rbac_config)
        
        if tiene_perm:
            emp = next((e for e in empleados if e['id'] == emp_id), None)
            if emp:
                empleados_con_permiso.append({
                    'empleado': emp['nombre'],
                    'rol': rol,
                    'nivel': nivel
                })
    
    return empleados_con_permiso


def audit_access(empleado_id, permiso_solicitado, rbac_config):
    """Audita intento de acceso"""
    tiene_perm, rol, nivel = check_permission(empleado_id, permiso_solicitado, rbac_config)
    
    audit_log = {
        'empleado_id': empleado_id,
        'permiso_solicitado': permiso_solicitado,
        'rol': rol,
        'nivel': nivel,
        'acceso_concedido': tiene_perm,
        'timestamp': '2024-04-13'
    }
    
    return audit_log


def generate_rbac_report(rbac_config, empleados):
    """Genera reporte de permisos"""
    report = {
        'total_roles': len(rbac_config['roles']),
        'total_asignaciones': len(rbac_config['asignaciones']),
        'roles_detalle': [],
        'permisos_criticos': {}
    }
    
    # Detalles por rol
    for rol in rbac_config['roles']:
        empleados_en_rol = [
            e['empleado_id'] for e in rbac_config['asignaciones']
            if e['rol'] == rol['nombre']
        ]
        report['roles_detalle'].append({
            'nombre': rol['nombre'],
            'nivel': rol['nivel'],
            'cantidad_empleados': len(empleados_en_rol),
            'permisos': rol['permisos']
        })
    
    # Permisos críticos
    critical_permissions = [
        'acceder_baticueva',
        'ver_todo',
        'gestionar_nomina',
        'eliminar_empleados'
    ]
    
    for perm in critical_permissions:
        report['permisos_criticos'][perm] = get_empleados_con_permiso(perm, rbac_config, empleados)
    
    return report


if __name__ == "__main__":
    from hr_manager import load_empleados
    
    empleados = load_empleados()
    rbac = load_rbac_config()
    
    print("=" * 60)
    print("🔐 SISTEMA RBAC - Control de Acceso")
    print("=" * 60)
    
    # Verificar permisos de algunos empleados
    test_cases = [
        ('EMP001', 'acceder_baticueva'),  # Alfred - Admin
        ('EMP006', 'acceder_baticueva'),  # Guardia - No debería
        ('EMP006', 'ver_camaras'),        # Guardia - Sí debería
        ('EMP009', 'editar_empleados'),   # Interno - No debería
    ]
    
    print("\n🧪 Pruebas de permisos:")
    for emp_id, permiso in test_cases:
        tiene_perm, rol, nivel = check_permission(emp_id, permiso, rbac)
        emp = next((e for e in empleados if e['id'] == emp_id), None)
        status = "✅ PERMITIDO" if tiene_perm else "❌ DENEGADO"
        print(f"   {emp['nombre']} ({rol}) -> {permiso}: {status}")
    
    # Reporte RBAC
    report = generate_rbac_report(rbac, empleados)
    
    print(f"\n📊 Configuración RBAC:")
    print(f"   Total roles: {report['total_roles']}")
    print(f"   Empleados con rol asignado: {report['total_asignaciones']}")
    
    print(f"\n🏢 Distribución de roles:")
    for rol in report['roles_detalle']:
        print(f"   {rol['nombre']} (Nivel {rol['nivel']}): {rol['cantidad_empleados']} empleados")
        print(f"      Permisos: {', '.join(rol['permisos'][:3])}...")
    
    print(f"\n🔑 Acceso a permisos críticos:")
    for perm, emps in report['permisos_criticos'].items():
        print(f"   {perm}: {len(emps)} empleados")
```

---

### Paso 6: Reporte HTML

**`scripts/report_generator.py`:**

```python
"""
Generador de reporte HTML de RRHH
"""
from hr_manager import load_empleados, load_turnos, generar_reporte_empleados, calcular_bonificacion
from rbac_system import load_rbac_config, get_empleado_rol


def generate_html_report(output_path='reports/reporte_rrhh.html'):
    """Genera reporte HTML completo"""
    
    empleados = load_empleados()
    turnos = load_turnos()
    rbac = load_rbac_config()
    reporte = generar_reporte_empleados(empleados)
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Wayne Manor - Recursos Humanos</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-value {{ font-size: 32px; font-weight: bold; }}
        .stat-label {{ font-size: 14px; opacity: 0.9; margin-top: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #34495e; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f9f9f9; }}
        .badge {{ padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; }}
        .admin {{ background: #e74c3c; color: white; }}
        .supervisor {{ background: #f39c12; color: white; }}
        .empleado {{ background: #3498db; color: white; }}
        .seguridad {{ background: #9b59b6; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏛️ Wayne Manor - Sistema de RRHH</h1>
        <p>Generado: 2024-04-13</p>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">{reporte['total_empleados']}</div>
                <div class="stat-label">Total Empleados</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{reporte['activos']}</div>
                <div class="stat-label">Empleados Activos</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">${reporte['promedio_salario']:,.0f}</div>
                <div class="stat-label">Salario Promedio</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">${reporte['costo_total_nomina']:,.0f}</div>
                <div class="stat-label">Costo Total Mensual</div>
            </div>
        </div>
        
        <h2>👥 Personal de Wayne Manor</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Rol</th>
                <th>Departamento</th>
                <th>Salario</th>
                <th>Acceso</th>
            </tr>
"""
    
    for emp in empleados:
        rol = get_empleado_rol(emp['id'], rbac['asignaciones'])
        badge_class = rol if rol in ['administrador', 'supervisor', 'empleado', 'seguridad'] else 'empleado'
        
        html += f"""
            <tr>
                <td>{emp['id']}</td>
                <td>{emp['nombre']}</td>
                <td>{emp['rol']}</td>
                <td>{emp['departamento']}</td>
                <td>${emp['salario_mensual']:,.2f}</td>
                <td><span class="badge {badge_class}">{rol}</span></td>
            </tr>
"""
    
    html += """
        </table>
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"✅ Reporte HTML generado: {output_path}")


if __name__ == "__main__":
    generate_html_report()
```

---

## Trabajo en Git

```bash
# Cambiar a tu rama
git checkout perez

# Agregar archivos
git add perez_rrhh/
git commit -m "feat: agrega sistema RRHH con RBAC para Wayne Manor"
git push origin perez
```

---

## Checklist

- [ ] Crear estructura de carpetas
- [ ] Archivo `empleados.csv` con 10+ registros
- [ ] Archivo `turnos.csv` configurado
- [ ] Sistema `rbac_system.py` funcionando
- [ ] `hr_manager.py` con reportes
- [ ] Reporte HTML generado
- [ ] Sistema RBAC valida permisos correctamente
- [ ] Subir a GitHub

---

## Integración con Accounts

Tu sistema RBAC puede vincularse con el sistema de usuarios de Django:

```python
# accounts/views.py - Verificar permisos
from django.contrib.auth.decorators import permission_required

@permission_required('accounts.view_admin')
def admin_dashboard(request):
    # Solo administradores pueden acceder
    ...
```

Contacto: **Nicolás** - Coordinación
