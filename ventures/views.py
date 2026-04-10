from django.shortcuts import render


def home(request):
    return render(request, 'ventures/home.html')


def about(request):
    return render(request, 'ventures/about.html')
