import pkg_resources

# There is probably a better way to handle static files outside Django
# but until then, I'll be using pkg_resources
PACKAGE_DIR = pkg_resources.resource_filename('git', '')
