# 🦇 Wayne Enterprises — Django Project
## Informe Estratégico: Transformación Digital y Migración a la Nube

## INSTALACIÓN

```bash
pip install django pillow
cd waynetech
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata core/fixtures/initial_data.json
python manage.py createsuperuser
python manage.py runserver
```

Abrir: http://127.0.0.1:8000/
Admin: http://127.0.0.1:8000/admin/

## IMÁGENES
Copiar JPGs a:
- media/team/      → Bruce, Lucius, Alfred, Barbara, Tim, Dick...
- media/gadgets/   → Batimóvil, Traje, Batwing...
- media/villains/  → Joker, Bane, Ra's, Nygma...
- media/divisions/ → Logos de cada división (opcional)

Luego asignar en el Admin → cada modelo tiene campo "image".

## SECCIONES
1. Hero — estadísticas globales de la empresa
2. Corporativo — ficha empresarial y contexto estratégico
3. Organigrama — CEO + 7 C-levels con perfil cloud (click = modal)
4. Divisiones — 7 unidades de negocio con prioridad cloud (click = modal)
5. Tecnología — gadgets filtrados por tipo (click = ficha técnica)
6. Amenazas — villanos filtrados por nivel/estado (click = expediente)
7. Estrategia Cloud — modelos operativos, CCoE, fases migración, Matriz RACI
8. KPIs — 10 indicadores agrupados por pilar estratégico con barras de progreso
