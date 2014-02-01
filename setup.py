from distutils.core import setup
setup(name='swehockey',
      version='1.1',
      py_modules=['swehockey'],
      description='Reads stats from swehockey.se',
      author='Peter Stark',
      author_email='peterstark72@gmail.com',
      url='https://github.com/peterstark72/swehockey',
      requires=['lxml'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: Free for non-commercial use',
          'Natural Language :: English',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities'
          ],
      )