#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from Public.drivers import Drivers
from Public.report import backup_monkey_report
from Public.maxim_monkey import Maxim
import unittest
from Demo.test_case import login_steps

"""
执行Maxim
tv.panda.test.monkey.Monkey
"""

if __name__ == '__main__':
    # 备份旧的测试报告文件夹到Backup下
    backup_monkey_report('./Backup', './MaximReport')

    package = 'com.taiwu.find'
    maximTime = 2  # 分钟
    cases = unittest.TestSuite()
    cases.addTest(login_steps.abcd('test_login_user'))

    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    command = Maxim().command(package=package, runtime=maximTime, mode='',
                              throttle=500,
                              options=' -v -v ', whitelist=True)
    print(command)

    # 稳定性测试
    Drivers().run_maxim(cases=cases, command=command, actions=True, widget_black=True)
