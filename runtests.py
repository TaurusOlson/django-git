#!/usr/bin/env python
import sys
import django
from django.conf import settings
from django.test.utils import get_runner


def configure():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'git',
        ),
        SECRET_KEY='fake-key',
    )


if not settings.configured: 
    configure()


def runtests():
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['git', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
