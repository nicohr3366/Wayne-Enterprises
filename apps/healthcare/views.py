from django.shortcuts import render
from .models import CyberSecurityRecord


def home(request):
    return render(request, 'healthcare/home.html')


def cybersecurity_dashboard(request):

    records = CyberSecurityRecord.objects.all()

    return render(
    request,
    'healthcare/cybersecurity_dashboard.html',
    {
        'records': records,
        'total_records': records.count(),
        'critical_count': records.filter(severity='CRÍTICA').count(),
        'blocked_count': records.filter(severity__in=['CRÍTICA', 'ALTA']).count(),
        'resolved_count': records.filter(severity='BAJA').count(),
    }
)
