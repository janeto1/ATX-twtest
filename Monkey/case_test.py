#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from Public.drivers import Drivers
import unittest
from Demo.test_case import login_steps

"""
单元测试CASE
"""
if __name__ == '__main__':
    cases = unittest.TestSuite()
    cases.addTest(login_steps.abcd('test_solopi'))

    # 功能单元测试
    Drivers().run_single_case(cases=cases)
