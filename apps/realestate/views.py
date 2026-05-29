import json
import csv
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum, Count, Avg, Q
from django.core.paginator import Paginator
from .models import Property


@login_required
def home(request):
    return render(request, 'realestate/home.html')


@login_required
def dashboard(request):
    total = Property.objects.count()

    if total == 0:
        return render(request, 'realestate/dashboard.html', {'sin_datos': True})

    total_value = Property.objects.aggregate(t=Sum('market_value_usd'))['t'] or 0
    avg_occupancy = (
        Property.objects.filter(project_status__in=['completed', 'active'])
        .aggregate(avg=Avg('occupancy_rate'))['avg'] or 0
    )
    in_development = Property.objects.filter(
        project_status__in=['under_construction', 'planned']
    ).count()

    def qs_to_json(qs, label_key, value_key):
        return json.dumps([
            {label_key: str(r[label_key] or ''), value_key: float(r[value_key] or 0)}
            for r in qs
        ])

    by_type = (Property.objects.values('property_type')
               .annotate(count=Count('id')).order_by('-count'))

    by_district = (Property.objects.values('district')
                   .annotate(count=Count('id')).order_by('-count')[:12])

    by_status = (Property.objects.values('project_status')
                 .annotate(count=Count('id')).order_by('-count'))

    by_developer = (Property.objects.values('developer')
                    .annotate(count=Count('id')).order_by('-count')[:10])

    by_year = (Property.objects.exclude(year_built__isnull=True)
               .values('year_built').annotate(count=Count('id')).order_by('year_built'))

    by_value = (Property.objects.values('property_type')
                .annotate(total=Sum('market_value_usd')).order_by('-total'))

    green_count = Property.objects.filter(green_certified=True).count()
    smart_count = Property.objects.filter(smart_building=True).count()
    available_count = Property.objects.filter(available=True).count()

    context = {
        'total': total,
        'total_value_b': round(float(total_value) / 1_000_000_000, 2),
        'avg_occupancy': round(float(avg_occupancy), 1),
        'in_development': in_development,

        'by_type_json': qs_to_json(by_type, 'property_type', 'count'),
        'by_district_json': qs_to_json(by_district, 'district', 'count'),
        'by_status_json': qs_to_json(by_status, 'project_status', 'count'),
        'by_developer_json': qs_to_json(by_developer, 'developer', 'count'),
        'by_year_json': qs_to_json(by_year, 'year_built', 'count'),
        'by_value_json': qs_to_json(by_value, 'property_type', 'total'),

        'green_pct': round(green_count / total * 100, 1),
        'smart_pct': round(smart_count / total * 100, 1),
        'available_pct': round(available_count / total * 100, 1),
    }
    return render(request, 'realestate/dashboard.html', context)


@login_required
def properties_list(request):
    qs = Property.objects.all()

    prop_type = request.GET.get('type', '')
    district = request.GET.get('district', '')
    status = request.GET.get('status', '')
    available = request.GET.get('available', '')
    search = request.GET.get('search', '')

    if prop_type:
        qs = qs.filter(property_type=prop_type)
    if district:
        qs = qs.filter(district=district)
    if status:
        qs = qs.filter(project_status=status)
    if available:
        qs = qs.filter(available=(available == '1'))
    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(location__icontains=search) |
            Q(developer__icontains=search)
        )

    total_filtrado = qs.count()
    paginator = Paginator(qs.order_by('-market_value_usd'), 20)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    districts = Property.objects.values_list('district', flat=True).distinct().order_by('district')
    statuses = Property.objects.values_list('project_status', flat=True).distinct().order_by('project_status')

    context = {
        'page_obj': page_obj,
        'districts': districts,
        'statuses': statuses,
        'current_type': prop_type,
        'current_district': district,
        'current_status': status,
        'current_available': available,
        'current_search': search,
        'total_filtrado': total_filtrado,
    }
    return render(request, 'realestate/list.html', context)


@login_required
def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    return render(request, 'realestate/detail.html', {'prop': prop})


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="propiedades_gotham.csv"'
    response.write('﻿')  # BOM para Excel

    qs = Property.objects.all()
    if request.GET.get('type'):
        qs = qs.filter(property_type=request.GET['type'])
    if request.GET.get('district'):
        qs = qs.filter(district=request.GET['district'])
    if request.GET.get('status'):
        qs = qs.filter(project_status=request.GET['status'])

    writer = csv.writer(response)
    writer.writerow([
        'PROJECT_ID', 'NAME', 'DEVELOPER', 'PROPERTY_TYPE', 'DISTRICT', 'LOCATION',
        'AREA_SQFT', 'FLOORS', 'YEAR_BUILT', 'PRICE_USD', 'MARKET_VALUE_USD',
        'OCCUPANCY_RATE', 'PROJECT_STATUS', 'GREEN_CERTIFIED', 'SMART_BUILDING',
        'ZONING_CODE', 'AVAILABLE',
    ])
    for p in qs:
        writer.writerow([
            p.project_id, p.name, p.developer, p.property_type, p.district, p.location,
            p.area_sqft, p.floors, p.year_built, p.price_usd, p.market_value_usd,
            p.occupancy_rate, p.project_status,
            'Sí' if p.green_certified else 'No',
            'Sí' if p.smart_building else 'No',
            p.zoning_code,
            'Sí' if p.available else 'No',
        ])
    return response
