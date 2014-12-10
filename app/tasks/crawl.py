import os
import subprocess

from ..models import package
from ..models import dependency
from ..lib.refresh_packages import refresh_packages


# Update the channel git repo
dirname = os.path.dirname(os.path.abspath(__file__))
dirname = os.path.join(dirname, '..', '..', 'channel')
dirname = os.path.realpath(dirname)

git_binary = None
for dir_ in os.environ['PATH'].split(os.pathsep):
    path = os.path.join(dir_, 'git')
    if os.path.exists(path):
        git_binary = path
        break

args = [git_binary, 'pull', 'origin', 'master']
proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT, cwd=dirname)
output, _ = proc.communicate()
print(output.decode(encoding='utf-8'))


# Limit each run to 400 packages
valid_sources = package.sources.outdated_sources(60, 400)
invalid_sources = package.sources.invalid_sources(valid_sources)

valid_dependency_sources = dependency.outdated_sources(60, 400)
invalid_dependency_sources = dependency.invalid_sources(valid_dependency_sources)

affected_packages, affected_dependencies = refresh_packages(invalid_sources, invalid_dependency_sources)

print('AFFECTED PACKAGES')
print(affected_packages)
print('\nAFFECTED DEPENDENCIES')
print(affected_dependencies)
