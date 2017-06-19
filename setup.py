from distutils.core import setup

setup(name='gdxcompare',
      version='0.1.2',
      description='Visually compare time series across GAMS GDX files',
      url='https://github.com/jackjackk/gdxcompare',
      author='Giacomo Marangoni',
      author_email='jackjackk@gmail.com',
      license='MIT',
      keywords='gdx gams dataviz',
      packages=['gdxcompare',],
      package_data={'gdxcompare':['*.html', '*.js']},
      install_requires=['gdxpy>=0.1.2'],
)
