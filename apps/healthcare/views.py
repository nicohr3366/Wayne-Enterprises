from django.shortcuts import render
from .models import CyberSecurityRecord


def home(request):
    return render(request, 'healthcare/home.html')


def cybersecurity_dashboard(request):

    records = CyberSecurityRecord.objects.all()

    return render(
        request,
        'healthcare/cybersecurity_dashboard.html',
        {'records': records}
    )