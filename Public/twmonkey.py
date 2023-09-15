#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

import uiautomator2 as u2
from logzero import logger
import time
import os

from Public.basepage import BasePage
from Public.decorator import *
from uiautomator2 import UiObjectNotFoundError

from Public.log import Log
from Public.config import maxin_path

log = Log()


class TWMonkey(BasePage):

    @classmethod
    def command(cls, package, runcnt, seed=None, throttle=False, pct_option=False, log_mode=None):
        '''
        monkey命令封装
        :param package:被测app的包名
        :param runcnt: 运行次数
        :param seed 种子
        :param throttle 延时时间
        :param pct_option 事件
        :param log_mode 日志模式
        :return: shell命令
        '''
        classpath = 'monkey'
        package = ' -p ' + package
        seed = ' -s ' + str(seed) if seed else ' '
        log_mode = ' ' + log_mode if log_mode else ' '
        throttle = ' --throttle ' + str(throttle) + ' ' if throttle else ' '
        # throttle = ' --throttle ' + str(throttle) + ' --randomize-throttle ' if throttle else ' '
        pct_option_str = ' '.join(pct_option) if len(pct_option) > 0 else ' '
        igonre_motion = ' --ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes'
        runcnt = ' ' + str(runcnt) if runcnt else ' '

        # 初始化日志目录
        off_line_cmd = ' >/sdcard/monkeyout.txt 2>/sdcard/monkeyerr.txt &'
        monkey_shell = (
            ''.join(
                [classpath, package, seed, throttle, pct_option_str, igonre_motion, log_mode, runcnt, off_line_cmd]))
        return monkey_shell

    @classmethod
    def run_monkey(cls, monkey_shell, excute_time):
        '''
        清理旧的配置文件并运行monkey，等待运行时间后pull log文件到电脑
        :param monkey_shell: shell命令 uiautomatortroy 时 max.xpath.selector文件需要配置正确
        :param actions: 特殊事件序列 max.xpath.actions文件需要配置正确
        :param widget_black: 黑控件 黑区域屏蔽 max.widget.black文件需要配置正确
        :return:
        '''
        log.i('MONKEY_SHELL:%s' % monkey_shell)
        cls.clear_env()
        log.i('starting run TWmonkey')
        log.i('It will be take about %s minutes,please be patient ...........................' % excute_time)
        # restore uiautomator server
        cls.d.service('uiautomator').stop()
        time.sleep(2)
        cls.d.shell(monkey_shell)
        time.sleep(int(excute_time) * 60 + 30)
        log.i('Maxim monkey run end>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # restore uiautomator server
        cls.d.service('uiautomator').start()

    @classmethod
    def clear_env(cls):
        log.i('Clearing monkey env')
        cls.d.shell('rm -r /sdcard/monkeyerr.txt')
        cls.d.shell('rm -r /sdcard/monkeyout.txt')
        log.i('Clear monkey env success')


if __name__ == '__main__':
    log.set_logger('udid', './log.log')
    mon = TWMonkey()
    mon.set_driver(None)
    excute_time = 2
    pct_option = ['--pct-touch 30', '--pct-motion 20']
    command = mon.command(package='com.taiwu.find', runcnt=100, seed=100, throttle=1000, pct_option=pct_option,
                          log_mode=' -v -v -v ', logpath='/sdcard/max-output')
    mon.run_monkey(command, excute_time)
