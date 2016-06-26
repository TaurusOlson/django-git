from django.conf.urls import url

from . import views

app_name = 'git'
urlpatterns = [
        # URL: /git/
        url(r'^$', views.index, name='index'),

        # URL: /git/<project_name>/commits_by_day/
        url(r'^(?P<name>[a-zA-Z-._0-9]+)/commits_by_day/$', views.commits_by_day, name='commits_by_day'),

        # Detailed view of a project
        # example: /git/5/
        url(r'^(?P<name>[a-zA-Z-._0-9]+)/$', views.detail, name='detail'),
]
