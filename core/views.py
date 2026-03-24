from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Division, Executive, Gadget, Villain, CloudKPI


def index(request):
    divisions  = Division.objects.all()
    executives = Executive.objects.filter(is_active=True)
    gadgets    = Gadget.objects.all()
    villains   = Villain.objects.all()
    kpis       = CloudKPI.objects.all()

    stats = {
        'divisiones':             divisions.count(),
        'gadgets_activos':        gadgets.filter(status='activo').count(),
        'villanos_detenidos':     villains.filter(status='detenido').count(),
        'amenazas_neutralizadas': sum(g.threat_neutralized for g in gadgets),
        'empleados_globales':     14200,
        'ingresos':               '31.7B USD',
    }

    # Filtros
    clasificacion  = request.GET.get('clasificacion', '')
    nivel          = request.GET.get('nivel', '')
    estado_villano = request.GET.get('estado', '')

    gadgets_f  = gadgets.filter(classification=clasificacion) if clasificacion else gadgets
    villains_f = villains.filter(threat_level=nivel) if nivel else villains
    if estado_villano:
        villains_f = villains_f.filter(status=estado_villano)

    # KPIs agrupados por pilar
    kpi_pillars = {}
    for kpi in kpis:
        p = kpi.get_pillar_display()
        kpi_pillars.setdefault(p, []).append(kpi)

    return render(request, 'core/index.html', {
        'divisions': divisions, 'executives': executives,
        'gadgets': gadgets_f, 'villains': villains_f,
        'kpis': kpis, 'kpi_pillars': kpi_pillars,
        'stats': stats,
        'clasificacion_activa': clasificacion,
        'nivel_activo': nivel,
        'estado_villano_activo': estado_villano,
        'clasificaciones': Gadget.CLASSIFICATION_CHOICES,
        'niveles_amenaza': Villain.THREAT_CHOICES,
        'estados_villano': Villain.STATUS_CHOICES,
        'total_villains': villains.count(),
    })


def division_detail(request, pk):
    d = get_object_or_404(Division, pk=pk)
    return JsonResponse({
        'id': d.pk, 'name': d.name, 'focus': d.focus,
        'description': d.description, 'cloud_relevance': d.cloud_relevance,
        'cloud_priority': d.get_cloud_priority_display(),
        'image': d.image.url if d.image else None,
    })


def executive_detail(request, pk):
    e = get_object_or_404(Executive, pk=pk)
    return JsonResponse({
        'id': e.pk, 'role': e.role, 'full_title': e.full_title,
        'name': e.name, 'level': e.get_level_display(),
        'strategic_responsibilities': e.strategic_responsibilities,
        'cloud_role': e.cloud_role, 'employee_id': e.employee_id,
        'image': e.image.url if e.image else None,
    })


def gadget_detail(request, pk):
    g = get_object_or_404(Gadget, pk=pk)
    return JsonResponse({
        'id': g.pk, 'name': g.name, 'code': g.code,
        'classification': g.get_classification_display(),
        'description': g.description, 'specs': g.specs,
        'status': g.get_status_display(), 'year_developed': g.year_developed,
        'threat_neutralized': g.threat_neutralized,
        'clearance_level': g.clearance_level,
        'image': g.image.url if g.image else None,
    })


def villain_detail(request, pk):
    v = get_object_or_404(Villain, pk=pk)
    return JsonResponse({
        'id': v.pk, 'name': v.name, 'alias': v.alias,
        'threat_level': v.get_threat_level_display(), 'threat_code': v.threat_level,
        'status': v.get_status_display(), 'status_code': v.status,
        'crimes': v.crimes, 'description': v.description,
        'times_detained': v.times_detained,
        'last_detained': str(v.last_detained) if v.last_detained else None,
        'arkham_cell': v.arkham_cell,
        'image': v.image.url if v.image else None,
    })
