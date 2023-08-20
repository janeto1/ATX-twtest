#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from Public.drivers import Drivers
from Public.report import *
from Public.maxim_monkey import Maxim
import unittest
from Monkey import login_steps
from Public.config import ensure_path

if __name__ == '__main__':
    # back up old report dir 备份旧的测试报告文件夹到TestReport_backup下
    data = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    # backup_report('./MaximReport')
    cases = unittest.TestSuite()
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    logpath = f'/sdcard/max-output/{current_time}'

    cases.addTest(login_steps.abcd('test_install_login'))
    command = Maxim().command(package='com.agentplusstudio', runtime=1, mode=None,
                              throttle=500,
                              options=' -v -v ', whitelist=True, logpath=logpath)
    print(command)

    Drivers().run_maxim(cases=cases, command=command, actions=True, widget_black=False, logpath=logpath)
