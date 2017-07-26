# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 12:47:52 2017

@author: casari
"""

import numpy
import logging
import os

__author__ = 'Matt Casari'

# Use Semantic Versioning, http://semver.org
from ._version import get_versions
__version__ = get_version()['version']
del get_version

def _setup_log():
    
    from icm import _debug
    logger = logging.getLogger('usb')