from django.shortcuts import render, get_object_or_404
from apps.realestate.models import UrbanProject


def home(request):
    return render(request, 'realestate/home.html')

def dashboard(request):

    projects = UrbanProject.objects.all()
    
    completed = UrbanProject.objects.filter(status='Completado').count()
    review = UrbanProject.objects.filter(status='En Revisión').count()
    suspended = UrbanProject.objects.filter(status='Suspendido').count()
    cancelled = UrbanProject.objects.filter(status='Cancelado').count()
    
    context = {
        'projects': projects,
        'completed': completed,
        'review': review,
        'suspended': suspended,
        'cancelled': cancelled,
    }

    return render(request, 'realestate/dashboard.html', context)

def projects_list(request):

    projects = UrbanProject.objects.all()

    return render(request, 'realestate/projects_list.html', {
        'projects': projects
    })


def project_detail(request, project_id):

    project = get_object_or_404(
        UrbanProject,
        project_id=project_id
    )

    return render(request, 'realestate/project_detail.html', {
        'project': project
    })