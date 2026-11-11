from django.shortcuts import render
from .models import StudentProject

def project_list(request):
    projects = StudentProject.objects.filter(is_published=True)
    return render(request, 'projects/list.html', {'projects': projects})