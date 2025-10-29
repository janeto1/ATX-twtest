# !/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from Public.drivers import Drivers
from Public.twfastbot import TWfastBot
from Public.report import backup_monkey_report
import unittest
from Demo.test_case import login_steps

"""
执行FastBot
"""

if __name__ == '__main__':
    # 备份旧的测试报告文件夹到Backup下
    backup_monkey_report('./Backup', './FastbotReport')
    package = 'com.taiwu.find'
    maximTime = 240 # 分钟
    cases = unittest.TestSuite()
    cases.addTest(login_steps.abcd('test_login_user'))

    command = TWfastBot().command(package=package, runtime=maximTime,
                                  throttle=500,
                                  options=' -v -v ', whitelist=True)
    print(command)

    # 稳定性测试
    Drivers().run_fastbot(cases=cases, command=command, actions=True, widget_black=True)
