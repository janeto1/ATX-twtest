#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from Public.drivers import Drivers
from Public.twmonkey import TWMonkey
import unittest
from Demo.test_case import login_steps
from Public.report import backup_monkey_report

"""
执行原生Monkey
"""
if __name__ == '__main__':
    # 备份旧的测试报告文件夹到Backup下
    backup_monkey_report('./Backup','./TWmonkeyReport')
    package = 'com.zhihu.android'
    log_mode = '-v -v -v '
    pct_option = []  # ['--pct-touch 30', '--pct-motion 20']
    seed = 1000
    runcnt = 20000
    throttle = 1000
    excute_time = int(runcnt / 60)

    cases = unittest.TestSuite()
    cases.addTest(login_steps.abcd('test_login_user'))

    command = TWMonkey.command(package=package, runcnt=runcnt, seed=seed, throttle=throttle, pct_option=pct_option,
                               log_mode=log_mode)
    print(command)

    # 稳定性测试
    Drivers().run_twmonkey(cases=cases, command=command, excute_time=excute_time)
