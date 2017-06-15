from distutils.core import setup

setup(name='gdxcompare',
      version='0.1.0',
      description='Visually compare time series in GAMS GDX files',
      url='https://github.com/jackjackk/gdxcompare',
      author='Giacomo Marangoni',
      author_email='jackjackk@gmail.com',
      license='MIT',
      keywords='gdx gams dataviz',
      packages=['gdxcompare',],
      install_requires=['gdxpy'],
)
