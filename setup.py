from distutils.core import setup

setup(name='dadaportal',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Dada management',
      url='http://dada.pink/dadaportal/',
      packages=['dadaportal'],
      install_requires = [
          'horetu>=0.1.0',

          'PyYAML>=3.11',
          'lxml>=3.4.2',
          'Jinja2>=2.8',

          'docutils>=0.12',
          'Markdown>=2.6.1'
      ],
      tests_require = [
          'pytest>=2.6.4',
      ],
      version='0.0.0',
      license='AGPL',
      entry_points = {
          'console_scripts': ['dadaportal = dadaportal:dadaportal']
      },
)
