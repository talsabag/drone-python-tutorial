import re
from setuptools import setup, find_packages

with open('service/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name="simple-service",
    version=version,
    author_email="josebarn@cisco.com",
    description="Drone + Python Demo Package.",
    long_description=open('README.md').read(),
    license="Apache 2.0 License",
    keywords="drone ci python example",
    url='https://github.com/josebarn/drone-python-tutorial',
    install_requires=['flask', 'alembic', 'sqlalchemy==0.9.8', 'psycopg2'],
    entry_points={
        'console_scripts': [
            'simple-service = service.run:cli_entry',
        ]
    },
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(exclude=("tests",)),
    package_data={'': ['LICENSE', '*.txt', '*.md', 'migrations/*']},
    tests_require=['nose'],
    test_suite='nose.collector',
)
