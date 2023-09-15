#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Public.drivers import Drivers

"""
执行solox
"""

def excute_solox(package,soloxTime):
    Drivers().run_solox_android(package=package, duration=soloxTime)
