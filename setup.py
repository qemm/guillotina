from setuptools import find_packages, setup

setup(
    name='plone.server',
    version=open('VERSION').read().strip(),
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGELOG.rst').read()),
    py_modules=[
        'plone.server',
    ],
    setup_requires=[
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['plone'],
    include_package_data=True,
    install_requires=[
        'aiohttp',
        'resolver_deco',
        'BTrees',
        'cchardet',
        'setuptools',
        'transaction',
        'plone.registry',
        'zope.component',
        'venusianconfiguration',
        'zope.configuration',
        'ZODB',
        'zope.component',
        'zope.configuration',
        'zope.interface',
        'zope.event',
        'zope.dottedname',
        'zope.i18nmessageid',
        'zope.i18n',
        'zope.location',
        'zope.security',
        'zope.schema',
        'plone.dexterity',
    ],
    tests_require=[
    ],
    entry_points={
        'console_scripts': [
            'sandbox = plone.server.server:main',
        ]
    }
)
