from setuptools import setup, find_packages
import os

version = '1.3'

def read(rnames):
    setupdir =  os.path.dirname( os.path.abspath(__file__))
    return open(
        os.path.join(setupdir, *rnames)
    ).read()

README =read((os.path.dirname(__file__),'README.txt')) +\
        read((os.path.dirname(__file__),
              'src', 'dj', 'paste','paste',
              'docs', 'README.txt'))
CHANGELOG  = read((os.path.dirname(__file__),
                      'docs', 'HISTORY.txt'))
TESTS  = read((os.path.dirname(__file__),
               'src', 'dj', 'paste','paste',
               'doctests', 'README.txt'))
long_description = '\n'.join([README, TESTS,CHANGELOG])+'\n\n'
setup(name='dj.paste',
      version=version,
      description="Yet another WSGI Paste factory for paste",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Mathieu Pasquet',
      author_email='kiorky@cryptelium.net',
      url='http://git.minitage.org/git/others/dj.paste',
      license='GPL',
      namespace_packages=['dj', 'dj.paste'],
      include_package_data=True,
      zip_safe=False,
      packages=find_packages('src'),
      extras_require={'test': ['ipython', 'zope.testing', ]},
      package_dir = {'': 'src'},
      install_requires=[
          'setuptools',
          'WebOb',
          'Werkzeug',
          'PasteScript',
          'Django',
      ],
      entry_points={
          'paste.app_factory': ['main=dj.paste.paste:django_factory',
                               ],
          'paste.filter_factory': ['debug=dj.paste.paste:debug_factory',
                                  ]
      },
     )
