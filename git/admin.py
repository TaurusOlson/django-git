from django.contrib import admin

from .models import Project, Commit


# class CommitInline(admin.StackedInline):
#     model = Commit
#     extra = 3


class CommitInline(admin.TabularInline):
    model = Commit
    extra = 3


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Start date', {'fields': ['first_time']}),
        ('Latest update', {'fields': ['last_time']}),
    ]
    inlines = [CommitInline]
    list_display = ('name', 'first_time', 'last_time', 'commits_count')
    list_filter = ['first_time', 'last_time']
    search_fields = ['name']

admin.site.register(Project, ProjectAdmin)

# Register your models here.
