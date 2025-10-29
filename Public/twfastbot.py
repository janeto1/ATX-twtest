#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from Public.decorator import *
from Public.log import Log
from Public.config import fastbot_path, fastbot_path_libs

log = Log()


# 参考网站：
# Fastbot-高速 Android Monkey 工具使用记录： https://testerhome.com/topics/11884
# 基于 Android Monkey 二次开发，实现高速点击的 Android Monkey 自动化工具 fastmonkey ：https://testerhome.com/topics/11719


class TWfastBot(BasePage):

    @classmethod
    def command(cls, package, runtime, whitelist=False, blacklist=False, throttle=None, options=None, off_line=True):
        '''
        monkey命令封装
        :param package:被测app的包名
        :param runtime: 运行时间 minutes分钟
        :param mode: 运行模式
            --agent reuseq  遍历模式，无需更改
        :param whitelist: activity白名单  需要将awl.strings 配置正确
        :param blacklist: activity黑名单  需要将awl.strings 配置正确
        :param throttle: 在事件之间插入固定的时间（毫秒）延迟
        :param options: 其他参数及用法同原始Monkey
        :param off_line: 是否脱机运行 默认Ture
        :return: shell命令
        '''
        classpath = 'CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/fastbot-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey'
        package = ' -p ' + package
        runtime = ' --running-minutes ' + str(runtime)
        mode = ' --agent reuseq'
        if throttle:
            throttle = ' --throttle ' + str(throttle)
        else:
            throttle = ''
        if options:
            options = ' ' + options
        else:
            options = ''

        if whitelist:
            whitelist = ' --act-whitelist-file /sdcard/awl.strings'
        else:
            whitelist = ''
        if blacklist:
            blacklist = ' --act-blacklist-file /sdcard/awl.strings'
        else:
            blacklist = ''
        # bug_report = f' --bugreport --output-directory {logpath}/crash.log'
        # 初始化日志目录
        off_line_cmd = ' >/sdcard/monkeyout.txt 2>/sdcard/monkeyerr.txt &'
        if off_line:
            monkey_shell = (
                ''.join([classpath, package, mode, whitelist, blacklist, runtime, throttle, options,
                         off_line_cmd]))
        else:
            monkey_shell = (
                ''.join([classpath, package, mode, whitelist, blacklist, runtime, throttle, options]))

        return monkey_shell

    @classmethod
    def run_monkey(cls, monkey_shell, actions=False, widget_black=False):
        '''
        清理旧的配置文件并运行monkey，等待运行时间后pull log文件到电脑
        :param monkey_shell: shell命令 uiautomatortroy 时 max.xpath.selector文件需要配置正确
        :param actions: 特殊事件序列 max.xpath.actions文件需要配置正确
        :param widget_black: 黑控件 黑区域屏蔽 max.widget.black文件需要配置正确
        :return:
        '''
        log.i('MONKEY_SHELL:%s' % monkey_shell)
        cls.clear_env()
        cls.push_jar()
        cls.set_logcat_size()
        if monkey_shell.find('awl.strings') != -1:
            cls.push_white_list()
        if monkey_shell.find('uiautomatortroy') != -1:
            cls.push_selector()
        if actions:
            cls.push_actions()
        if widget_black:
            cls.push_widget_black()
        cls.set_AdbIME()
        runtime = monkey_shell.split('running-minutes ')[1].split(' ')[0]
        log.i('starting run monkey')
        log.i('It will be take about %s minutes,please be patient ...........................' % runtime)
        # restore uiautomator server
        cls.d.service('uiautomator').stop()
        time.sleep(2)
        cls.d.shell(monkey_shell)
        time.sleep(int(runtime) * 60 + 30)
        log.i('Fastbot monkey run end>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # restore uiautomator server
        cls.d.service('uiautomator').start()

    @classmethod
    def push_jar(cls):
        cls.d.push(os.path.join(fastbot_path, 'monkeyq.jar'), '/sdcard/monkeyq.jar')
        cls.d.push(os.path.join(fastbot_path, 'framework.jar'), '/sdcard/framework.jar')
        cls.d.push(os.path.join(fastbot_path, 'fastbot-thirdpart.jar'), '/sdcard/fastbot-thirdpart.jar')
        cls.d.push(os.path.join(fastbot_path_libs, 'arm64-v8a', 'libfastbot_native.so'), '/data/local/tmp/arm64-v8a/')
        cls.d.push(os.path.join(fastbot_path_libs, 'armeabi-v7a', 'libfastbot_native.so'),
                   '/data/local/tmp/armeabi-v7a/')
        cls.d.push(os.path.join(fastbot_path_libs, 'x86', 'libfastbot_native.so'), '/data/local/tmp/x86/')
        cls.d.push(os.path.join(fastbot_path_libs, 'x86_64', 'libfastbot_native.so'), '/data/local/tmp/x86_64/')
        log.i('push fastbot config file--->monkeyq.jar framework.jar fastbot-thirdpart.jar libs')

    @classmethod
    def push_white_list(cls):
        cls.d.push(os.path.join(fastbot_path, 'awl.strings'), '/sdcard/awl.strings')
        log.i('push white_list file---> awl.strings ')

    @classmethod
    def push_actions(cls):
        cls.d.push(os.path.join(fastbot_path, 'max.xpath.actions'), '/sdcard/max.xpath.actions')
        log.i('push actions file---> max.xpath.actions ')

    @classmethod
    def push_selector(cls):
        cls.d.push(os.path.join(fastbot_path, 'max.xpath.selector'), '/sdcard/max.xpath.selector')
        log.i('push selector file---> max.xpath.selector ')

    @classmethod
    def push_widget_black(cls):
        cls.d.push(os.path.join(fastbot_path, 'max.widget.black'), '/sdcard/max.widget.black')
        log.i('push widget_black file---> max.widget.black ')

    @classmethod
    def push_string(cls):
        cls.d.push(os.path.join(fastbot_path, 'max.strings'), '/sdcard/max.strings')
        log.i('push string file---> max.strings ')

    @classmethod
    def set_logcat_size(cls):
        cls.d.shell('logcat -G 10MB')
        log.i('set logcat cache size---> 10MB ')

    @classmethod
    def clear_env(cls):
        log.i('Clearing monkey env')
        cls.d.shell('rm -r /sdcard/max.widget.black')
        cls.d.shell('rm -r /sdcard/max.xpath.selector')
        cls.d.shell('rm -r /sdcard/max.xpath.actions')
        cls.d.shell('rm -r /sdcard/awl.strings')
        cls.d.shell('rm -r /sdcard/monkeyq.jar')
        cls.d.shell('rm -r /sdcard/framework.jar')
        cls.d.shell('rm -r /sdcard/fastbot-thirdpart.jar')
        cls.d.shell('rm -r /sdcard/max.strings')
        cls.d.shell('rm -r /data/local/tmp/arm64-v8a')
        cls.d.shell('rm -r /data/local/tmp/armeabi-v7a')
        cls.d.shell('rm -r /data/local/tmp/x86')
        cls.d.shell('rm -r /data/local/tmp/x86_64')
        cls.d.shell('rm -r /sdcard/monkeyerr.txt')
        cls.d.shell('rm -r /sdcard/monkeyout.txt')
        log.i('Clear fastbot env success')

    @classmethod
    def set_AdbIME(cls):
        log.i('setting AdbIME as default')
        ime = cls.d.shell('ime list -a').output
        if 'adbkeyboard' in ime:
            cls.d.shell('ime set com.android.adbkeyboard/.AdbIME')
        else:
            cls.local_install(os.path.join(fastbot_path, 'ADBKeyBoard.apk'))
            cls.d.shell('ime enable com.android.adbkeyboard/.AdbIME')
            cls.d.shell('ime set com.android.adbkeyboard/.AdbIME')
            log.i('install adbkeyboard and set as default')
        cls.push_string()


if __name__ == '__main__':
    log.set_logger('udid', './log.log')
    Fastbot = Fastbot()
    Fastbot.set_driver(None)
    command = Fastbot.command(package='com.quvideo.xiaoying', runtime=2, mode=None, throttle=100,
                              options=' -v -v ', whitelist=True, off_line=True, logpath='D:/code/ATX-Test/log')
    Fastbot.run_monkey(command)
