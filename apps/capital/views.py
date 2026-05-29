import json
import csv
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Avg, Count, Sum, Min, Max
from django.core.paginator import Paginator
from .models import StockRecord


@login_required
def home(request):
    total = StockRecord.objects.count()
    return render(request, 'capital/home.html', {'total': total})


@login_required
def dashboard(request):
    total_records = StockRecord.objects.count()

    if total_records == 0:
        return render(request, 'capital/dashboard.html', {'sin_datos': True})

    tickers = StockRecord.objects.values('ticker').distinct().count()
    avg_close = StockRecord.objects.aggregate(a=Avg('close_price'))['a'] or 0
    date_min = StockRecord.objects.aggregate(d=Min('date'))['d']
    date_max = StockRecord.objects.aggregate(d=Max('date'))['d']

    # Chart data: avg close by ticker
    by_ticker = (StockRecord.objects.values('ticker')
                 .annotate(avg_close=Avg('close_price'))
                 .order_by('-avg_close')[:15])

    # Chart data: count by sector
    by_sector = (StockRecord.objects.values('sector')
                 .annotate(count=Count('id'))
                 .order_by('-count'))

    # Price evolution: top 5 tickers by avg close
    top5 = [r['ticker'] for r in by_ticker[:5]]
    evolution_data = {}
    for ticker in top5:
        qs = (StockRecord.objects.filter(ticker=ticker)
              .values('date', 'close_price')
              .order_by('date'))
        evolution_data[ticker] = [
            {'date': str(r['date']), 'close': float(r['close_price'])} for r in qs
        ]

    # Volume by ticker
    by_volume = (StockRecord.objects.values('ticker')
                 .annotate(total_vol=Sum('volume'))
                 .order_by('-total_vol')[:10])

    # Market cap by division
    by_division = (StockRecord.objects.values('division')
                   .annotate(avg_cap=Avg('market_cap_usd'))
                   .order_by('-avg_cap'))

    context = {
        'total_records': total_records,
        'tickers': tickers,
        'avg_close': round(float(avg_close), 2),
        'date_min': date_min,
        'date_max': date_max,
        'by_ticker_json': json.dumps([
            {'ticker': r['ticker'], 'avg_close': round(float(r['avg_close']), 2)}
            for r in by_ticker
        ]),
        'by_sector_json': json.dumps([
            {'sector': r['sector'], 'count': r['count']}
            for r in by_sector
        ]),
        'evolution_json': json.dumps(evolution_data),
        'by_volume_json': json.dumps([
            {'ticker': r['ticker'], 'total_vol': r['total_vol']}
            for r in by_volume
        ]),
        'by_division_json': json.dumps([
            {'division': r['division'], 'avg_cap': round(float(r['avg_cap']) / 1e9, 2)}
            for r in by_division
        ]),
    }
    return render(request, 'capital/dashboard.html', context)


@login_required
def stocks_list(request):
    qs = StockRecord.objects.all()

    ticker_f = request.GET.get('ticker', '')
    sector_f = request.GET.get('sector', '')
    exchange_f = request.GET.get('exchange', '')
    search_f = request.GET.get('search', '')

    if ticker_f:
        qs = qs.filter(ticker=ticker_f)
    if sector_f:
        qs = qs.filter(sector=sector_f)
    if exchange_f:
        qs = qs.filter(exchange=exchange_f)
    if search_f:
        qs = qs.filter(company_name__icontains=search_f) | qs.filter(ticker__icontains=search_f)

    total_filtrado = qs.count()
    paginator = Paginator(qs.order_by('-date', 'ticker'), 50)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    tickers = StockRecord.objects.values_list('ticker', flat=True).distinct().order_by('ticker')
    sectors = StockRecord.objects.values_list('sector', flat=True).distinct().order_by('sector')
    exchanges = StockRecord.objects.values_list('exchange', flat=True).distinct().order_by('exchange')

    context = {
        'page_obj': page_obj,
        'tickers': tickers,
        'sectors': sectors,
        'exchanges': exchanges,
        'current_ticker': ticker_f,
        'current_sector': sector_f,
        'current_exchange': exchange_f,
        'current_search': search_f,
        'total_filtrado': total_filtrado,
    }
    return render(request, 'capital/list.html', context)


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="wayne_stocks.csv"'
    response.write('﻿')

    qs = StockRecord.objects.all()
    if request.GET.get('ticker'):
        qs = qs.filter(ticker=request.GET['ticker'])
    if request.GET.get('sector'):
        qs = qs.filter(sector=request.GET['sector'])

    writer = csv.writer(response)
    writer.writerow([
        'TICKER', 'COMPANY', 'DIVISION', 'DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE',
        'ADJ_CLOSE', 'VOLUME', 'MARKET_CAP_USD', 'PE_RATIO', 'DIVIDEND_YIELD',
        'SECTOR', 'EXCHANGE'
    ])
    for r in qs:
        writer.writerow([
            r.ticker, r.company_name, r.division, r.date,
            r.open_price, r.high_price, r.low_price, r.close_price,
            r.adj_close, r.volume, r.market_cap_usd, r.pe_ratio,
            r.dividend_yield, r.sector, r.exchange
        ])
    return response
