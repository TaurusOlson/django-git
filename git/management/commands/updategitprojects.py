# Django
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# Python
from pathlib import Path
import sys

# Application
from git.utils import update_database, is_git_project
from git.models import Project, Commit


if not hasattr(settings, 'PROJECTS_DIR'):
    print("Please define PROJECTS_DIR in settings.py")
    sys.exit(1)
elif not Path(settings.PROJECTS_DIR).expanduser().is_dir():
    print("Can't find the directory {0} defined with PROJECTS_DIR.".format(settings.PROJECTS_DIR))
    sys.exit(1)



# INIT
projects_dir = Path(settings.PROJECTS_DIR).expanduser()
projects = filter(is_git_project, projects_dir.iterdir())


class Command(BaseCommand):
    help = 'Updates the database'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write("Updating the database...")
        for project in projects:
            update_database(project)
        self.stdout.write("Number of projects: {0}".format(Project.objects.all().count()))
