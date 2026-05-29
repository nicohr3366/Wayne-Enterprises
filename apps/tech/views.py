import json
import csv
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Avg, Count, Sum, Min, Max
from django.core.paginator import Paginator
from .models import TumblerTelemetry


@login_required
def home(request):
    total = TumblerTelemetry.objects.count()
    return render(request, 'tech/home.html', {'total': total})


@login_required
def dashboard(request):
    total_records = TumblerTelemetry.objects.count()

    if total_records == 0:
        return render(request, 'tech/dashboard.html', {'sin_datos': True})

    vehicles = TumblerTelemetry.objects.values('vehicle_id').distinct().count()
    missions = TumblerTelemetry.objects.values('mission_id').distinct().count()
    alerts = TumblerTelemetry.objects.exclude(alert_type='none').exclude(alert_type='').count()

    # By vehicle model
    by_model = (TumblerTelemetry.objects.values('vehicle_model')
                .annotate(count=Count('id'))
                .order_by('-count'))

    # By mission type
    by_mission = (TumblerTelemetry.objects.values('mission_type')
                  .annotate(count=Count('id'))
                  .order_by('-count'))

    # By alert type (donut)
    by_alert = (TumblerTelemetry.objects.values('alert_type')
                .annotate(count=Count('id'))
                .order_by('-count'))

    # By gotham zone
    by_zone = (TumblerTelemetry.objects.values('gotham_zone')
               .annotate(count=Count('id'))
               .order_by('-count')[:10])

    # Avg speed by mission type
    avg_speed = (TumblerTelemetry.objects.values('mission_type')
                 .annotate(avg_spd=Avg('speed_kmh'))
                 .order_by('-avg_spd'))

    # Fuel distribution bins
    fuel_ranges = {
        '0-25%': TumblerTelemetry.objects.filter(fuel_level_pct__lt=25).count(),
        '25-50%': TumblerTelemetry.objects.filter(fuel_level_pct__gte=25, fuel_level_pct__lt=50).count(),
        '50-75%': TumblerTelemetry.objects.filter(fuel_level_pct__gte=50, fuel_level_pct__lt=75).count(),
        '75-100%': TumblerTelemetry.objects.filter(fuel_level_pct__gte=75).count(),
    }

    context = {
        'total_records': total_records,
        'vehicles': vehicles,
        'missions': missions,
        'alerts': alerts,
        'by_model_json': json.dumps([
            {'model': r['vehicle_model'], 'count': r['count']} for r in by_model
        ]),
        'by_mission_json': json.dumps([
            {'mission': r['mission_type'], 'count': r['count']} for r in by_mission
        ]),
        'by_alert_json': json.dumps([
            {'alert': r['alert_type'] or 'none', 'count': r['count']} for r in by_alert
        ]),
        'by_zone_json': json.dumps([
            {'zone': r['gotham_zone'], 'count': r['count']} for r in by_zone
        ]),
        'avg_speed_json': json.dumps([
            {'mission': r['mission_type'], 'avg_spd': round(float(r['avg_spd'] or 0), 1)} for r in avg_speed
        ]),
        'fuel_json': json.dumps([
            {'range': k, 'count': v} for k, v in fuel_ranges.items()
        ]),
    }
    return render(request, 'tech/dashboard.html', context)


@login_required
def telemetry_list(request):
    qs = TumblerTelemetry.objects.all()

    model_f = request.GET.get('model', '')
    mission_f = request.GET.get('mission', '')
    alert_f = request.GET.get('alert', '')
    zone_f = request.GET.get('zone', '')

    if model_f:
        qs = qs.filter(vehicle_model=model_f)
    if mission_f:
        qs = qs.filter(mission_type=mission_f)
    if alert_f:
        qs = qs.filter(alert_type=alert_f)
    if zone_f:
        qs = qs.filter(gotham_zone=zone_f)

    total_filtrado = qs.count()
    paginator = Paginator(qs.order_by('-timestamp'), 50)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    models = TumblerTelemetry.objects.values_list('vehicle_model', flat=True).distinct().order_by('vehicle_model')
    missions = TumblerTelemetry.objects.values_list('mission_type', flat=True).distinct().order_by('mission_type')
    alerts = TumblerTelemetry.objects.values_list('alert_type', flat=True).distinct().order_by('alert_type')
    zones = TumblerTelemetry.objects.values_list('gotham_zone', flat=True).distinct().order_by('gotham_zone')

    context = {
        'page_obj': page_obj,
        'models': models,
        'missions': missions,
        'alerts': alerts,
        'zones': zones,
        'current_model': model_f,
        'current_mission': mission_f,
        'current_alert': alert_f,
        'current_zone': zone_f,
        'total_filtrado': total_filtrado,
    }
    return render(request, 'tech/list.html', context)


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="tumbler_telemetry.csv"'
    response.write('﻿')

    qs = TumblerTelemetry.objects.all()
    if request.GET.get('model'):
        qs = qs.filter(vehicle_model=request.GET['model'])

    writer = csv.writer(response)
    writer.writerow([
        'RECORD_ID', 'TIMESTAMP', 'VEHICLE_ID', 'VEHICLE_MODEL', 'MISSION_ID',
        'MISSION_TYPE', 'SPEED_KMH', 'FUEL_LEVEL_PCT', 'ENGINE_TEMP_C',
        'BATTERY_LEVEL_PCT', 'GOTHAM_ZONE', 'ALERT_TYPE', 'SYSTEM_STATUS', 'DISTANCE_KM'
    ])
    for r in qs:
        writer.writerow([
            r.record_id, r.timestamp, r.vehicle_id, r.vehicle_model, r.mission_id,
            r.mission_type, r.speed_kmh, r.fuel_level_pct, r.engine_temp_c,
            r.battery_level_pct, r.gotham_zone, r.alert_type, r.system_status, r.distance_km
        ])
    return response
