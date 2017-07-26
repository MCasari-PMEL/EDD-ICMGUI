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
version_info = (0,1,0)
__version__ = '%d.%d.%d' % version_info

def _setup_log():
    
    from icm import _debug
    logger = logging.getLogger('usb')