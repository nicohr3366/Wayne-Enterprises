import json
import csv
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.apps import apps as django_apps
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.core.paginator import Paginator
from .models import DefenseContract

DIVISION_APPS = [
    'apps.tech',
    'apps.industries',
    'apps.healthcare',
    'apps.realestate',
    'apps.capital',
    'apps.foundation',
    'apps.ventures',
]


@login_required
def home(request):
    apps_activas = [
        app.replace('apps.', '') for app in DIVISION_APPS
        if django_apps.is_installed(app)
    ]
    return render(request, 'core/home.html', {'apps_activas': apps_activas})


@login_required
def contracts_dashboard(request):
    total_records = DefenseContract.objects.count()

    if total_records == 0:
        return render(request, 'core/contracts_dashboard.html', {'sin_datos': True})

    total_obligated = DefenseContract.objects.aggregate(t=Sum('obligated_amount_usd'))['t'] or 0
    etl_systems = DefenseContract.objects.values('etl_source_system').distinct().count()
    xml_schemas = DefenseContract.objects.values('xml_schema_version').distinct().count()

    def qs_to_json(qs, label_key, value_key):
        return json.dumps([
            {label_key: str(r[label_key] or ''), value_key: float(r[value_key] or 0)}
            for r in qs
        ])

    by_agency = (DefenseContract.objects.values('agency')
                 .annotate(total=Sum('obligated_amount_usd')).order_by('-total')[:14])

    by_source = (DefenseContract.objects.values('etl_source_system')
                 .annotate(count=Count('id')).order_by('-count')[:17])

    by_year = (DefenseContract.objects.values('fiscal_year')
               .annotate(total=Sum('obligated_amount_usd')).order_by('fiscal_year'))

    by_security = (DefenseContract.objects.values('security_classification')
                   .annotate(count=Count('id')).order_by('-count'))

    by_status = (DefenseContract.objects.values('performance_status')
                 .annotate(count=Count('id')).order_by('-count'))

    by_format = (DefenseContract.objects.values('data_feed_format')
                 .annotate(count=Count('id')).order_by('-count'))

    top_contractors = (DefenseContract.objects.values('contractor_name')
                       .annotate(total=Sum('obligated_amount_usd')).order_by('-total')[:10])

    by_cmmc = (DefenseContract.objects.values('cyber_compliance_level')
               .annotate(count=Count('id')).order_by('-count'))

    top_naics = (DefenseContract.objects.values('naics_description')
                 .annotate(total=Sum('obligated_amount_usd')).order_by('-total')[:8])

    sb = DefenseContract.objects.filter(small_business=True).count()
    vet = DefenseContract.objects.filter(veteran_owned=True).count()
    women = DefenseContract.objects.filter(women_owned=True).count()
    hub = DefenseContract.objects.filter(hubzone=True).count()

    context = {
        'total_records': total_records,
        'total_obligated_b': round(float(total_obligated) / 1_000_000_000, 1),
        'etl_systems': etl_systems,
        'xml_schemas': xml_schemas,

        'by_agency_json': qs_to_json(by_agency, 'agency', 'total'),
        'by_source_json': qs_to_json(by_source, 'etl_source_system', 'count'),
        'by_year_json': qs_to_json(by_year, 'fiscal_year', 'total'),
        'by_security_json': qs_to_json(by_security, 'security_classification', 'count'),
        'by_status_json': qs_to_json(by_status, 'performance_status', 'count'),
        'by_format_json': qs_to_json(by_format, 'data_feed_format', 'count'),
        'top_contractors_json': qs_to_json(top_contractors, 'contractor_name', 'total'),
        'by_cmmc_json': qs_to_json(by_cmmc, 'cyber_compliance_level', 'count'),
        'top_naics_json': qs_to_json(top_naics, 'naics_description', 'total'),

        'sb_pct': round(sb / total_records * 100, 1),
        'vet_pct': round(vet / total_records * 100, 1),
        'women_pct': round(women / total_records * 100, 1),
        'hub_pct': round(hub / total_records * 100, 1),
    }
    return render(request, 'core/contracts_dashboard.html', context)


@login_required
def contracts_list(request):
    qs = DefenseContract.objects.all()

    agency = request.GET.get('agency', '')
    year = request.GET.get('year', '')
    status = request.GET.get('status', '')
    search = request.GET.get('search', '')

    if agency:
        qs = qs.filter(agency=agency)
    if year:
        qs = qs.filter(fiscal_year=year)
    if status:
        qs = qs.filter(performance_status=status)
    if search:
        qs = qs.filter(contractor_name__icontains=search) | qs.filter(contract_number__icontains=search)

    total_filtrado = qs.count()
    paginator = Paginator(qs.order_by('-obligated_amount_usd'), 50)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    agencies = DefenseContract.objects.values_list('agency', flat=True).distinct().order_by('agency')
    years = DefenseContract.objects.values_list('fiscal_year', flat=True).distinct().order_by('fiscal_year')
    statuses = DefenseContract.objects.values_list('performance_status', flat=True).distinct().order_by('performance_status')

    context = {
        'page_obj': page_obj,
        'agencies': agencies,
        'years': years,
        'statuses': statuses,
        'current_agency': agency,
        'current_year': year,
        'current_status': status,
        'current_search': search,
        'total_filtrado': total_filtrado,
    }
    return render(request, 'core/contracts_list.html', context)


@login_required
def contract_detail(request, pk):
    contract = get_object_or_404(DefenseContract, pk=pk)
    return render(request, 'core/contract_detail.html', {'contract': contract})


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="contratos_defensa.csv"'
    response.write('﻿')  # BOM para Excel

    qs = DefenseContract.objects.all()
    if request.GET.get('agency'):
        qs = qs.filter(agency=request.GET['agency'])
    if request.GET.get('year'):
        qs = qs.filter(fiscal_year=request.GET['year'])

    writer = csv.writer(response)
    writer.writerow([
        'CONTRACT ID', 'CONTRACT NUMBER', 'AGENCY', 'CONTRACTOR NAME',
        'OBLIGATED AMOUNT USD', 'FISCAL YEAR', 'PERFORMANCE STATUS',
        'ETL SOURCE SYSTEM', 'SECURITY CLASSIFICATION', 'NAICS CODE', 'NAICS DESCRIPTION',
        'CYBER COMPLIANCE LEVEL', 'SMALL BUSINESS', 'VETERAN OWNED', 'WOMEN OWNED', 'HUBZONE',
    ])
    for c in qs:
        writer.writerow([
            c.contract_id, c.contract_number, c.agency, c.contractor_name,
            c.obligated_amount_usd, c.fiscal_year, c.performance_status,
            c.etl_source_system, c.security_classification, c.naics_code, c.naics_description,
            c.cyber_compliance_level,
            'Sí' if c.small_business else 'No',
            'Sí' if c.veteran_owned else 'No',
            'Sí' if c.women_owned else 'No',
            'Sí' if c.hubzone else 'No',
        ])
    return response
