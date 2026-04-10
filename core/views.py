from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.apps import apps as django_apps

DIVISION_APPS = [
    'tech',
    'industries',
    'healthcare',
    'realestate',
    'capital',
    'foundation',
    'ventures',
]

@login_required
def home(request):

    apps_activas = [
        app for app in DIVISION_APPS
        if django_apps.is_installed(app)
    ]

    context = {
        'apps_activas': apps_activas,
    }
    
    return render(request, 'core/home.html', context)