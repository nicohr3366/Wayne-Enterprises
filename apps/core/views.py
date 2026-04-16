from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.apps import apps as django_apps

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

    context = {
        'apps_activas': apps_activas,
    }

    return render(request, 'core/home.html', context)