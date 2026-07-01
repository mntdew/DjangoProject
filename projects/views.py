from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Project, Category, Rating


def project_list(request):
    projects = Project.objects.all()
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    # Фильтрация по категории
    if category_id:
        projects = projects.filter(category_id=category_id)

    # ПОЛНОТЕКСТОВЫЙ ПОИСК POSTGRESQL
    if query:
        # Настройка вектора: название важнее описания (вес A против B)
        vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
        search_query = SearchQuery(query)
        projects = projects.annotate(
            rank=SearchRank(vector, search_query)
        ).filter(rank__gte=0.05).order_by('-rank')  # Сортировка по релевантности

    categories = Category.objects.all()
    return render(request, 'projects/project_list.html', {
        'projects': projects,
        'categories': categories,
        'query': query,
        'selected_category': int(category_id) if category_id else None
    })


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # Проверка, голосовал ли уже пользователь (по сессии)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    has_rated = Rating.objects.filter(project=project, session_key=session_key).exists()

    if request.method == 'POST' and 'rating' in request.POST and not has_rated:
        score = int(request.POST.get('rating'))
        Rating.objects.create(project=project, score=score, session_key=session_key)
        return redirect('project_detail', pk=pk)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'has_rated': has_rated
    })