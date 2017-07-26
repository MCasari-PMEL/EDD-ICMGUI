# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='ICM',
      version='',
      description='Interface Control Module',
      author='Matt Casari',
      author_email='matthew.casari@noaa.gov',
      #python_requires='>=3',
      url='https://github.com/NOAA-PMEL/EDD-ICMGUI',
      classifiers= [
              "Programming Language :: Python 3.5",
              "Development Status :: 2 - Pre-Alpha",
              "Intended Audience :: End Users/Desktop",
              "Intended Audience :: Science/Research",
              "License :: OSI Approved :: MIT License",
              "Operating System :: Microsoft :: Windows :: Windows 7",
              "Topic :: Scientific/Engineering :: Visualization",
              "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
              "Topic :: Scientific/Engineering :: Human Machine Interfaces",
              "Topic :: System :: Hardware :: Hardware Drivers",
              "Topic :: Software Development :: User Interfaces",],
      requires=['numpy','scipy']

     )