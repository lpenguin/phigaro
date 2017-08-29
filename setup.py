from setuptools import setup

setup(name='phigaro',
      description='Phigaro is a scalable command-line tool for predictions phages and prophages '
                  'from nucleid acid sequences (including metagenomes).'
                  'It is based on phage genes HMMs and a smoothing window algorithm.',
      version=open("phigaro/_version.py").readlines()[-1].split()[-1].strip("\"'"),
      author='E.Starikova, N.Pryanichnikov',
      author_email='hed.robin@gmail.com',
      url='https://github.com/lpenguin/phigaro',
      packages=['phigaro',
                'phigaro.finder',
                'phigaro.cli',
                'phigaro.scheduling',
                'phigaro.scheduling.task',
                'phigaro.misc',
                ],
      entry_points={
          'console_scripts': [
              'phigaro = phigaro.cli.batch:main',
              'phigaro-setup = phigaro.cli.helper:main',
          ]
      },
      install_requires=['six', 'sh>=1.12.0', 'singleton', 'PyYAML', 'future', 'numpy']
      )
