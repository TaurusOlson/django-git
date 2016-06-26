"""Useful functions"""

# Django
from django.conf import settings
from django.db.models import Count
from django.utils import timezone

# Python 
import os
from pathlib import Path, PosixPath
from hashlib import sha1
from random import randint, sample


# Third-party
import pygal 
from pygal.style import BlueStyle
from pygal.config import Config
import pytz
from pygit2 import Repository, GitError, GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE

# Application
from git.models import Project, Commit
from . import PACKAGE_DIR


# HELPERS
def fromtimestamp(ts):
    return timezone.datetime.fromtimestamp(ts).replace(tzinfo=pytz.utc)


def get_commits(repo):
    try:
        head = repo.head
    except GitError:
        print("Repository {0} has no head".format(repo))
        commits = []
    else:
        commits = repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL)
    return commits


def githash():
    """Simple function returning a random Git SHA1"""
    data = ''.join(sample(list(map(chr, range(122))), 60))
    data = bytes(data, 'utf-8')
    s = sha1(data)
    return s.hexdigest()


def get_head_commit(repo):
    return repo.revparse_single('HEAD')


def is_git_project(path):
    """Simple assumption on a git project: it must contain a .git directory"""
    if not isinstance(path, PosixPath):
        path = Path(path)
    return (path / '.git').is_dir()


def create_project_record(repo):
    """Create a project record from the input Git repository

    Parameters:
    data - Repository
        The input data

    Returns:
    project_record - models.Project
        
    """
    path_parts = repo.path.split(os.sep)
    i = path_parts.index('.git') - 1
    name = path_parts[i]

    # Number of commits
    commits = list(get_commits(repo))
    commits_count = len(commits)
    if commits_count == 0:
        return None

    # Project
    head = commits[0]
    initial = commits[-1]
    first_time = fromtimestamp(initial.commit_time)
    last_time = fromtimestamp(head.commit_time)
    author = get_project_author(repo)

    project_record = Project(name=name, author=author, 
            first_time=first_time, last_time=last_time,
            commits_count=commits_count)

    return project_record


def update_project_table(project_record):
    # Insert if project was not already in the projects
    if project_record.name not in [p.name for p in Project.objects.all()]:
        project_record.save()
    # If it is already in the projects
    else:
        # and it was updated
        cur_project_in_db = Project.objects.get(name=project_record.name)
        if cur_project_in_db.was_updated(project_record):
            project_record.save()


def update_database(project_path):
    """Update the database with the project at the given path

    Parameters:
    project_path - Path
        A `Path` instance to the Git project

    Returns:
    None
    """
    p = project_path / '.git'
    repo = Repository(p.as_posix())
    project_record = create_project_record(repo)
    if project_record:
        update_project_table(project_record)
        create_commit_records(repo, project_record)


def get_project_author(repo):
    """Return the name of the author of the project

    The author of the project is assumed to be the author of the first
    commit in the master branch

    :param repo: 
        a :class:`pygit2.Repository` instance

    :returns: 
        The name of the author

    """
    target = repo.lookup_branch('master').target
    first_commit = next(repo.walk(target, GIT_SORT_TOPOLOGICAL | GIT_SORT_REVERSE))
    return first_commit.author.name


def create_commit_record(commit, project):
    """Create a models.Commit instance from a pygit2.Commit instance

    :commit: pygit2.Commit
        A commit object

    :param project: models.Project
        A Project record

    :returns: models.Commit
        A Commit record

    """
    commit_record =  Commit(sha=str(commit.id), commit_time=fromtimestamp(commit.commit_time), 
            message=commit.message, committer=commit.committer.name,
            project_id=project)
    commit_record.save()
    return commit_record


def create_commit_records(repo, project):
    """@todo: Docstring for create_commit_records.

    :arg1: @todo
    :returns: @todo

    """
    for commit in get_commits(repo):
        create_commit_record(commit, project)



def dmap(fn, record):
    """map for a dictionary

    :param fn: a function
    :param record: a dictionary
    :returns: a dictionary

    """
    record_type = type(record)
    values = (fn(v) for k, v in record.items())
    return record_type(zip(record, values))


def get_readme(directory):
    """Return the text of the README contained in the given directory

    :directory: The directory
    :returns: the text of the README file

    """
    dir_content = Path(directory).expanduser().iterdir()
    files = filter(lambda x: x.name.upper().startswith("README"), dir_content)
    files = list(files)

    if len(files) == 1:
        with files[0].open() as f:
            readme = f.read()
    else:
        readme = 'No README file available'
    return readme


def count_commits_by_committer(project):
    """Count the number of commits for each committer

    :param project: A Project instance
    :returns commits_count_by_committer: The QuerySet with the number of
    commits by committer

    """
    commits_count_by_committer = project.commit_set.values('committer') \
        .annotate(count=Count('sha')) \
        .order_by('-count')
    return commits_count_by_committer


def make_bar_chart(title, label, data, width=960, height=400):
    """Make a bar chart with given data and the appropriate style 

    :param title: The title of the chart
    :param label: The label of the chart
    :param data: The data
    :param width: The width of the chart
    :param data: The height of the chart
    :returns chart:
    """
    # Chart style
    custom_style = BlueStyle
    custom_style.background = "transparent"
    custom_style.plot_background = "transparent"
    custom_style.major_guide_stroke_dasharray = '0,0'
    custom_style.guide_stroke_dasharray = '0,0'

    # Chart config
    css_style = Path(PACKAGE_DIR).joinpath('static/git/css/graph.css')
    config = Config()
    config.css.append('file://' + css_style.as_posix())
    print(config.css)

    chart = pygal.Bar(config)
    chart.width = 960
    chart.height = 400
    chart.style = custom_style
    chart.show_y_guides=True
    chart.show_x_guides=False
    chart.explicit_size=True 
    chart.title = title
    chart.add('Count', data[0:20])
    return chart
