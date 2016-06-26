# Django
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

# Python
import datetime

# Application
from .models import Project


class ProjectMethodTests(TestCase):
    """Testing the methods of the Project model"""

    def test_was_updated_with_updated_project(self):
        """was_updated should return True if the project was updated"""
        project_cur = Project(name='my_project')
        project_cur.last_time = timezone.now()
        project_new = Project(name='my_project')
        project_new.last_time = timezone.now() + datetime.timedelta(days=1)
        self.assertEqual(project_cur.was_updated(project_new), True)

    def test_was_updated_with_unchanged_project(self):
        """was_updated should return False if the project is unchanged"""
        project_cur = Project(name='my_project')
        project_cur.last_time = timezone.now()
        project = Project(name='my_project')
        project.last_time = project_cur.last_time
        self.assertEqual(project_cur.was_updated(project), False)

    def test_was_updated_with_outdated_project(self):
        """was_updated should return False if the project should be updated"""
        project_cur = Project(name='my_project')
        project_cur.last_time = timezone.now()
        project_old = Project(name='my_project')
        project_old.last_time = timezone.now() - datetime.timedelta(days=1)
        self.assertEqual(project_cur.was_updated(project_old), False)


# TODO Find out how to tests views in a reusable app
# class ProjectViewTests(TestCase):
#     """Testing the views related to the Project model"""

#     def test_index_view_with_no_project(self):
#         """If no projects exist, an appropriate messahe should be displayed"""
#         response = self.client.get(reverse('git:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'No projects found.')
#         self.assertQuerysetEqual(response.context['project_list'], [])
