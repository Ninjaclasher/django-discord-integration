from setuptools import find_packages, setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='django-discord-integration',
    version='1.0.1',
    author='Evan Zhang',
    install_requires=['requests', 'django-solo'],
    description='Discord integration for Django, supporting error reporting via webhooks.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/Ninjaclasher/django-discord-integration',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
)
