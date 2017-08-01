# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 13:54:00 2017

@author: casari
"""

from git import Repo
import semver
import os


def get_version():
#    pwd = os.getcwd()
#    pwd = pwd[0:pwd.rfind('\\')]
    repo = Repo('..')
    #repo = Repo(pwd)
    
    tag = repo.tags
    __version__ = []
    if len(tag) > 0:
        if tag[0] == 'v':
            tag = tag[1:]
        
        ver = semver.parse(tag)
        prerelease = repo.head.ref.commit.hexsha
        ver['prerelease'] = prerelease[0:6]
        
        __version__ = semver.format_version(ver['major'],ver['minor'],ver['patch'],ver['prerelease'])
        
    return __version__