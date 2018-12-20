from setuptools import setup

setup(name='mgdl',
      version='1.0',
      description='CLI Manga Downloader',
      keywords='cli anime manga downloader',
      url='https://github.com/FR0ST1N/mgdl',
      author='FR0ST1N',
      author_email='iamfrostin@gmail.com',
      license='MIT',
      packages=['mgdl'],
      zip_safe=False,
      entry_points = {
        'console_scripts': ['mgdl=mgdl.cli_entry:main'],
      },
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          ],
      install_requires=[
          'beautifulsoup4',
          'pyprind',
      ])