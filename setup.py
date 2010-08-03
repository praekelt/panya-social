from setuptools import setup, find_packages

setup(
    name='panya-social',
    version='0.0.1',
    description='Panya social app.',
    long_description = open('README.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/panya-social',
    packages = find_packages(),
    dependency_links = [
        'http://github.com/praekelt/django-socialregistration/tarball/0.4.1.tokenstore.1#egg=django-socialregistration-0.4.1.tokenstore.1',
        'http://github.com/facebook/python-sdk/tarball/master#egg=facebook-python-sdk',
        'http://github.com/praekelt/django-activity-stream/tarball/master#egg=django-activity-stream-0.2.1.praekelt',
        'http://github.com/pinax/django-friends/tarball/master#egg=django-friends-0.2.dev1',
        'http://github.com/pinax/django-notification/tarball/master#egg=django-notification-0.2.0.dev2',
    ],
    install_requires = [
        'django-activity-stream==0.2.1.praekelt',
        'django-friends==0.2.dev1',
        'django-notification==0.2.0.dev2',
        'django-socialregistration==0.4.1.tokenstore.1',
        'facebook-python-sdk',
        'panya',
    ],
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
