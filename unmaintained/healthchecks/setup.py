from setuptools import find_packages, setup

def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n')
                for l in f if l.strip('\n') and not l.startswith('#')]

setup(
    name = 'healthchecks',
    version = '1.0',
    license = 'BSD-3-Clause',
    packages = find_packages(exclude=['.*/tests/.*']),
    include_package_data = True,
    install_requires = parse_requirements('requirements.txt'),
)
