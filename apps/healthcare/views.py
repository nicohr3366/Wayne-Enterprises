import json
import csv
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import CyberSecurityRecord


@login_required
def home(request):
    return render(request, 'healthcare/home.html')


@login_required
def cybersecurity_dashboard(request):
    all_records = CyberSecurityRecord.objects.all()
    total_records = all_records.count()

    if total_records == 0:
        return render(request, 'healthcare/cybersecurity_dashboard.html', {'sin_datos': True})

    # Filtros
    severity = request.GET.get('severity', '')
    status   = request.GET.get('status', '')
    threat   = request.GET.get('threat', '')
    search   = request.GET.get('search', '')

    qs = all_records
    if severity:
        qs = qs.filter(severity=severity)
    if status:
        qs = qs.filter(status=status)
    if threat:
        qs = qs.filter(threat_type=threat)
    if search:
        qs = qs.filter(
            Q(incident_id__icontains=search) |
            Q(affected_system__icontains=search) |
            Q(threat_type__icontains=search)
        )

    total_filtrado = qs.count()
    paginator = Paginator(qs, 25)
    page_obj  = paginator.get_page(request.GET.get('page', 1))

    def qs_to_json(qs, label_key, value_key):
        return json.dumps([
            {label_key: str(r[label_key] or ''), value_key: int(r[value_key] or 0)}
            for r in qs
        ])

    by_severity = all_records.values('severity').annotate(count=Count('id')).order_by('-count')
    by_status   = all_records.values('status').annotate(count=Count('id')).order_by('-count')
    by_threat   = all_records.values('threat_type').annotate(count=Count('id')).order_by('-count')[:10]
    by_system   = all_records.values('affected_system').annotate(count=Count('id')).order_by('-count')[:10]

    context = {
        'page_obj':       page_obj,
        'total_records':  total_records,
        'total_filtrado': total_filtrado,
        'critical_count': all_records.filter(severity='Critical').count(),
        'blocked_count':  all_records.filter(severity__in=['Critical', 'High']).count(),
        'resolved_count': all_records.filter(status='Resolved').count(),

        'by_severity_json': qs_to_json(by_severity, 'severity',       'count'),
        'by_status_json':   qs_to_json(by_status,   'status',         'count'),
        'by_threat_json':   qs_to_json(by_threat,   'threat_type',    'count'),
        'by_system_json':   qs_to_json(by_system,   'affected_system','count'),

        'severities': all_records.values_list('severity',    flat=True).distinct().order_by('severity'),
        'statuses':   all_records.values_list('status',      flat=True).distinct().order_by('status'),
        'threats':    all_records.values_list('threat_type', flat=True).distinct().order_by('threat_type'),

        'current_severity': severity,
        'current_status':   status,
        'current_threat':   threat,
        'current_search':   search,
    }
    return render(request, 'healthcare/cybersecurity_dashboard.html', context)


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="ciberseguridad_healthcare.csv"'
    response.write('﻿')  # BOM para Excel

    qs = CyberSecurityRecord.objects.all()
    if request.GET.get('severity'):
        qs = qs.filter(severity=request.GET['severity'])
    if request.GET.get('status'):
        qs = qs.filter(status=request.GET['status'])

    writer = csv.writer(response)
    writer.writerow(['ID_Evento', 'Tipo_Evento', 'Severidad', 'Sistema_Afectado', 'Estado'])
    for r in qs:
        writer.writerow([r.incident_id, r.threat_type, r.severity, r.affected_system, r.status])
    return response
