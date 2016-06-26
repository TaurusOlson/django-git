# Django
from django.views import generic
from django.utils import timezone
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf.urls.static import static

# App
from .models import Project, Commit
from .utils import get_readme, make_bar_chart, count_commits_by_committer
from . import PACKAGE_DIR

# Python
from pathlib import Path


def index(request):
    """The index view shows the list of Git projects"""
    name = request.GET.get('name')
    author = request.GET.get('author')
    project_list = Project.objects.all()

    if name:
        project_list = project_list.filter(name__icontains=name)
    if author:
        project_list = project_list.filter(author__icontains=author)

    project_list = project_list.order_by('-last_time')
    context = {'project_list': project_list}
    return render(request, 'git/index.html', context)


def detail(request, name):
    """The detail view of the Git project"""
    project = get_object_or_404(Project, name=name)
    projects_dir = Path(settings.PROJECTS_DIR).expanduser()
    project_dir = projects_dir.joinpath(name)

    # Pagination: 50 commits per page
    paginator = Paginator(project.commit_set.all().order_by('-commit_time'), 50)
    page = request.GET.get('page')
    try:
        commits = paginator.page(page)
    # If page is not an integer
    except PageNotAnInteger:
        commits = paginator.page(1)
    # If page is out of range
    except EmptyPage:
        commits = paginator.page(paginator.num_pages)

    # Chart 1: chart of the number of commits by committer
    # Processing
    commits_count_by_committer = count_commits_by_committer(project)
    counts = [x['count'] for x in commits_count_by_committer]
    # Chart
    chart_title = 'Number of commits of the top 20 committers'
    chart = make_bar_chart(chart_title, 'Count', counts)

    svg_file = Path(PACKAGE_DIR).joinpath('static/git/charts/commits_count_by_committer.svg')
    chart.render_to_file(svg_file.as_posix())

    context = {'project': project, 'readme': get_readme(project_dir),
               'commits': commits}
               
    return render(request, 'git/detail.html', context)


def commits_by_day(request, name):
    """Number of commits by day for the given project """
    project = get_object_or_404(Project, name=name)
    context = {"project": project}
    return render(request, "git/commits_by_day.html", context)
