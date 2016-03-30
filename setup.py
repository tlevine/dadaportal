from distutils.core import setup

setup(name='dadaportal',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Dada management',
      url='http://dada.pink/dadaportal/',
      packages=['dadaportal'],
      install_requires = [
          'PyYAML>=3.11',
          'horetu>=0.1.0',
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
