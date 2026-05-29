import json
import csv
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Avg, Count, Sum, Min, Max
from django.core.paginator import Paginator
from .models import Donacion


@login_required
def home(request):
    total = Donacion.objects.count()
    return render(request, 'foundation/home.html', {'total': total})


@login_required
def dashboard(request):
    total_registros = Donacion.objects.count()

    if total_registros == 0:
        return render(request, 'foundation/dashboard.html', {'sin_datos': True})

    total_amount = Donacion.objects.aggregate(t=Sum('amount_usd'))['t'] or 0
    avg_amount = Donacion.objects.aggregate(a=Avg('amount_usd'))['a'] or 0

    # Top category
    top_cat_qs = (Donacion.objects.values('project_category')
                  .annotate(total=Sum('amount_usd'))
                  .order_by('-total').first())
    top_category = top_cat_qs['project_category'] if top_cat_qs else 'N/A'

    # By category
    by_category = (Donacion.objects.values('project_category')
                   .annotate(total=Sum('amount_usd'), count=Count('id'))
                   .order_by('-total'))

    # By donor type
    by_donor_type = (Donacion.objects.values('donor_type')
                     .annotate(total=Sum('amount_usd'), count=Count('id'))
                     .order_by('-total'))

    # By fiscal year
    by_year = (Donacion.objects.values('fiscal_year')
               .annotate(total=Sum('amount_usd'))
               .order_by('fiscal_year'))

    # By district
    by_district = (Donacion.objects.values('gotham_district')
                   .annotate(total=Sum('amount_usd'))
                   .order_by('-total')[:10])

    # Top 10 donors
    top_donors = (Donacion.objects.values('donor_name')
                  .annotate(total=Sum('amount_usd'))
                  .order_by('-total')[:10])

    context = {
        'total_registros': total_registros,
        'total_amount_m': round(float(total_amount) / 1_000_000, 1),
        'avg_amount': round(float(avg_amount) / 1000, 1),
        'top_category': top_category,
        'by_category_json': json.dumps([
            {'category': r['project_category'], 'total': round(float(r['total']) / 1000, 1), 'count': r['count']}
            for r in by_category
        ]),
        'by_donor_type_json': json.dumps([
            {'donor_type': r['donor_type'], 'total': round(float(r['total']) / 1000, 1), 'count': r['count']}
            for r in by_donor_type
        ]),
        'by_year_json': json.dumps([
            {'year': str(r['fiscal_year']), 'total': round(float(r['total']) / 1_000_000, 2)}
            for r in by_year if r['fiscal_year']
        ]),
        'by_district_json': json.dumps([
            {'district': r['gotham_district'], 'total': round(float(r['total']) / 1000, 1)}
            for r in by_district
        ]),
        'top_donors_json': json.dumps([
            {'donor': r['donor_name'], 'total': round(float(r['total']) / 1_000_000, 2)}
            for r in top_donors
        ]),
    }
    return render(request, 'foundation/dashboard.html', context)


@login_required
def donaciones_list(request):
    qs = Donacion.objects.all()

    categoria_f = request.GET.get('categoria', '')
    tipo_f = request.GET.get('tipo', '')
    year_f = request.GET.get('year', '')
    search_f = request.GET.get('search', '')

    if categoria_f:
        qs = qs.filter(project_category=categoria_f)
    if tipo_f:
        qs = qs.filter(donor_type=tipo_f)
    if year_f:
        qs = qs.filter(fiscal_year=year_f)
    if search_f:
        qs = qs.filter(donor_name__icontains=search_f) | qs.filter(project_name__icontains=search_f)

    total_filtrado = qs.count()
    paginator = Paginator(qs.order_by('-amount_usd'), 50)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    categorias = Donacion.objects.values_list('project_category', flat=True).distinct().order_by('project_category')
    tipos = Donacion.objects.values_list('donor_type', flat=True).distinct().order_by('donor_type')
    years = Donacion.objects.values_list('fiscal_year', flat=True).distinct().order_by('fiscal_year')

    context = {
        'page_obj': page_obj,
        'categorias': categorias,
        'tipos': tipos,
        'years': years,
        'current_categoria': categoria_f,
        'current_tipo': tipo_f,
        'current_year': year_f,
        'current_search': search_f,
        'total_filtrado': total_filtrado,
    }
    return render(request, 'foundation/list.html', context)


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="wayne_donaciones.csv"'
    response.write('﻿')

    qs = Donacion.objects.all()
    if request.GET.get('categoria'):
        qs = qs.filter(project_category=request.GET['categoria'])

    writer = csv.writer(response)
    writer.writerow([
        'DONATION_ID', 'DONOR_NAME', 'DONOR_TYPE', 'AMOUNT_USD', 'DONATION_DATE',
        'PROJECT_NAME', 'PROJECT_CATEGORY', 'GOTHAM_DISTRICT', 'FISCAL_YEAR',
        'TAX_DEDUCTIBLE', 'MATCHED', 'RECURRING', 'STATUS'
    ])
    for d in qs:
        writer.writerow([
            d.donation_id, d.donor_name, d.donor_type, d.amount_usd, d.donation_date,
            d.project_name, d.project_category, d.gotham_district, d.fiscal_year,
            d.tax_deductible, d.matched, d.recurring, d.status
        ])
    return response
