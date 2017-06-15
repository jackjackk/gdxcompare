from distutils.core import setup

setup(name='gdxcompare',
      version='0.1.1a',
      description='Visually compare time series across GAMS GDX files',
      url='https://github.com/jackjackk/gdxcompare',
      author='Giacomo Marangoni',
      author_email='jackjackk@gmail.com',
      license='MIT',
      keywords='gdx gams dataviz',
      packages=['gdxcompare',],
      install_requires=['gdxpy>=0.1.2'],
)
