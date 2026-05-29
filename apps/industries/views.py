import json
import csv
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Avg, Count, Sum, Min, Max
from django.core.paginator import Paginator
from .models import ElectricRecord


@login_required
def home(request):
    total = ElectricRecord.objects.count()
    return render(request, 'industries/home.html', {'total': total})


@login_required
def dashboard(request):
    total_records = ElectricRecord.objects.count()

    if total_records == 0:
        return render(request, 'industries/dashboard.html', {'sin_datos': True})

    stations = ElectricRecord.objects.values('station_id').distinct().count()
    total_generated = ElectricRecord.objects.aggregate(t=Sum('energy_generated_mwh'))['t'] or 0
    avg_renewable = ElectricRecord.objects.filter(renewable_pct__isnull=False).aggregate(a=Avg('renewable_pct'))['a'] or 0

    # Energy generated vs consumed by district
    by_district_gen = (ElectricRecord.objects.values('gotham_district')
                       .annotate(
                           generated=Sum('energy_generated_mwh'),
                           consumed=Sum('energy_consumed_mwh')
                       ).order_by('-generated')[:10])

    # By fuel type
    by_fuel = (ElectricRecord.objects.values('fuel_type')
               .annotate(total=Sum('energy_generated_mwh'), count=Count('id'))
               .order_by('-total'))

    # By station type
    by_station_type = (ElectricRecord.objects.values('station_type')
                       .annotate(count=Count('id'))
                       .order_by('-count'))

    # Renewable pct trend by year
    renewable_trend = (ElectricRecord.objects.values('fiscal_year')
                       .annotate(avg_ren=Avg('renewable_pct'))
                       .order_by('fiscal_year'))

    # Outage hours by district
    outage_by_district = (ElectricRecord.objects.values('gotham_district')
                          .annotate(total_out=Sum('outage_hours'))
                          .order_by('-total_out')[:10])

    context = {
        'total_records': total_records,
        'stations': stations,
        'total_generated_gwh': round(float(total_generated) / 1000, 1),
        'avg_renewable': round(float(avg_renewable), 1),
        'by_district_json': json.dumps([
            {
                'district': r['gotham_district'],
                'generated': round(float(r['generated'] or 0) / 1000, 2),
                'consumed': round(float(r['consumed'] or 0) / 1000, 2),
            }
            for r in by_district_gen
        ]),
        'by_fuel_json': json.dumps([
            {'fuel': r['fuel_type'], 'total': round(float(r['total'] or 0) / 1000, 2), 'count': r['count']}
            for r in by_fuel if r['fuel_type'] != 'n/a'
        ]),
        'by_station_type_json': json.dumps([
            {'type': r['station_type'], 'count': r['count']} for r in by_station_type
        ]),
        'renewable_trend_json': json.dumps([
            {'year': str(r['fiscal_year']), 'avg': round(float(r['avg_ren'] or 0), 1)}
            for r in renewable_trend if r['fiscal_year']
        ]),
        'outage_json': json.dumps([
            {'district': r['gotham_district'], 'hours': round(float(r['total_out'] or 0), 2)}
            for r in outage_by_district
        ]),
    }
    return render(request, 'industries/dashboard.html', context)


@login_required
def grid_list(request):
    qs = ElectricRecord.objects.all()

    district_f = request.GET.get('district', '')
    fuel_f = request.GET.get('fuel', '')
    type_f = request.GET.get('type', '')
    year_f = request.GET.get('year', '')

    if district_f:
        qs = qs.filter(gotham_district=district_f)
    if fuel_f:
        qs = qs.filter(fuel_type=fuel_f)
    if type_f:
        qs = qs.filter(station_type=type_f)
    if year_f:
        qs = qs.filter(fiscal_year=year_f)

    total_filtrado = qs.count()
    paginator = Paginator(qs.order_by('-date'), 50)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    districts = ElectricRecord.objects.values_list('gotham_district', flat=True).distinct().order_by('gotham_district')
    fuels = ElectricRecord.objects.values_list('fuel_type', flat=True).distinct().order_by('fuel_type')
    types = ElectricRecord.objects.values_list('station_type', flat=True).distinct().order_by('station_type')
    years = ElectricRecord.objects.values_list('fiscal_year', flat=True).distinct().order_by('fiscal_year')

    context = {
        'page_obj': page_obj,
        'districts': districts,
        'fuels': fuels,
        'types': types,
        'years': years,
        'current_district': district_f,
        'current_fuel': fuel_f,
        'current_type': type_f,
        'current_year': year_f,
        'total_filtrado': total_filtrado,
    }
    return render(request, 'industries/list.html', context)


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="gotham_electric_grid.csv"'
    response.write('﻿')

    qs = ElectricRecord.objects.all()
    if request.GET.get('district'):
        qs = qs.filter(gotham_district=request.GET['district'])

    writer = csv.writer(response)
    writer.writerow([
        'RECORD_ID', 'DATE', 'STATION_ID', 'STATION_NAME', 'GOTHAM_DISTRICT',
        'STATION_TYPE', 'ENERGY_GENERATED_MWH', 'ENERGY_CONSUMED_MWH',
        'PEAK_DEMAND_MW', 'AVG_DEMAND_MW', 'RENEWABLE_PCT', 'OUTAGE_HOURS',
        'FUEL_TYPE', 'FISCAL_YEAR'
    ])
    for r in qs:
        writer.writerow([
            r.record_id, r.date, r.station_id, r.station_name, r.gotham_district,
            r.station_type, r.energy_generated_mwh, r.energy_consumed_mwh,
            r.peak_demand_mw, r.avg_demand_mw, r.renewable_pct, r.outage_hours,
            r.fuel_type, r.fiscal_year
        ])
    return response
