from django.db import models

from django.utils import timezone


class Project(models.Model):
    """Git project"""
    name = models.CharField(primary_key=True, max_length=40)
    author = models.CharField(max_length=40, blank=True, null=True)
    first_time = models.DateTimeField()
    last_time = models.DateTimeField()
    commits_count = models.IntegerField()

    def __str__(self):
        return self.name

    def was_updated(self, project):
        """Return True if the project was updated.
        
        Compare the the last update time of the project with the last update
        time of the same project after updating the database.
        
        """
        # TODO: Find a better criterion to determine
        # that it's the same project with new updates
        if project.name == project.name:
            return project.last_time > self.last_time
        else:
            return False


class Commit(models.Model):
    """Commit in a Git project"""
    sha = models.CharField(primary_key=True, max_length=40)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    commit_time = models.DateTimeField()
    committer = models.CharField(max_length=40, blank=True, null=True)
    message = models.TextField()

    def __str__(self):
        return self.sha

