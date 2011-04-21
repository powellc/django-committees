from setuptools import setup, find_packages

setup(
    name='django-committees',
    version=__import__('committees').__version__,
    license="BSD",

    install_requires = [
        'django-markup-mixin',
        'django-extensions',
        'simple_history',
        'django-photologue',
        'django-eventy',],

    description='A simple reusable application for managing a small orgs governance in a Django application.',
    long_description=open('README.rst').read(),

    author='Colin Powell',
    author_email='colin@onecardinal.com',

    url='http://github.com/powellc/django-committees',
    download_url='http://github.com/powellc/django-committees/downloads',

    include_package_data=True,

    packages=['committees'],

    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
