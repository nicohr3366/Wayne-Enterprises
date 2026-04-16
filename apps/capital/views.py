from django.shortcuts import render


def home(request):
    return render(request, 'capital/home.html')
