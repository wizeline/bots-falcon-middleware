import re
from pip.req import parse_requirements
from setuptools import setup, find_packages


def requirements(filename):
    reqs = parse_requirements(filename, session=False)
    return [str(r.req) for r in reqs]


def get_version():
    with open('buzon/__init__.py', 'r') as f:
        version_regex = r'^__version__\s*=\s*[\'"](.+)[\'"]'
        return re.search(version_regex, f.read(), re.MULTILINE).group(1)

setup(
    name='bots-falcon-middleware',
    version=get_version(),
    url='https://github.com/wizeline/bots-falcon-middleware',
    author='Wizeline',
    author_email='engineering@wizeline.com',
    description='A bots platform library for the middlewares',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: Development',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python 3.6.2',
        'Topic :: Utilities'
    ],
    tests_require=requirements('requirements.txt'),
    install_requires=requirements('requirements.txt'),
)
