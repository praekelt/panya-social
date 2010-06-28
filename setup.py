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
        'http://github.com/flashingpumpkin/django-socialregistration/tarball/master#egg=django-socialregistration-0.4.1',
        'http://github.com/facebook/python-sdk/tarball/master#egg=facebook-python-sdk',
        'http://github.com/praekelt/django-activity-stream/tarball/master#egg=django-activity-stream-0.2.1.praekelt'
    ],
    install_requires = [
        'django-activity-stream==0.2.1.praekelt',
        'django-socialregistration==0.4.1',
        'facebook-python-sdk',
    ],
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Panya",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
