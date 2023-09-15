from multiprocessing.pool import ThreadPool
import time
import os
import traceback
import zipfile

from multiprocessing import Pool
import uiautomator2 as u2
from Public.devices_new import *
# from Public.Devices import *
from Public.RunCases import RunCases
from Public.RunMaxim import RunMaxim, RunTWmonkey
from Public.reportpath import ReportPath
from Public.basepage import BasePage
from Public.maxim_monkey import Maxim
from Public.log import Log
from Public.test_data import *
from Public.config import local_log_path, create_dir
from Public.report import *
from logzero import logger
from solox.public.apm import APM
from solox.public.common import Devices
from Public.twmonkey import TWMonkey
from Public.twfastbot import TWfastBot


# from Public.chromedriver import ChromeDriver


class Drivers:
    @staticmethod
    def _run_cases(run, cases, retry, save_last_try):
        log = Log()
        log.set_logger(run.get_device()['model'], run.get_path() + '/' + 'client.log')
        log.i('udid: %s' % run.get_device()['udid'])

        # set cls.path, it must be call before operate on any page
        path = ReportPath()
        path.set_path(run.get_path())

        # set cls.driver, it must be call before operate on any page
        base_page = BasePage()
        if 'ip' in run.get_device():
            base_page.set_driver(run.get_device()['ip'])
        else:
            base_page.set_driver(run.get_device()['serial'])

        try:
            # print(run.get_device())
            # 运行前准备
            base_page.unlock_device()
            base_page.set_fastinput_ime()  # 设置fastime输入法
            # base_page.d.shell('logcat -c')  # 清空logcat
            # 开始执行测试
            run.run(cases, retry, save_last_try)

            # 结束后操作
            base_page.unwatch_device()
            base_page.set_original_ime()

            # 将logcat文件上传到报告
            # base_page.d.shell('logcat -d > /sdcard/logcat.log')
            # time.sleep(2)
            # base_page.d.pull('/sdcard/logcat.log', os.path.join(path.get_path(), 'logcat.log'))

            if 'ip' in run.get_device():
                log.i('release device %s ' % run.get_device()['serial'])
                atxserver2().release_device(run.get_device()['serial'])

        except AssertionError as e:
            log.e('AssertionError, %s' % e)

    @staticmethod
    def _run_maxim(run, cases, command, actions, widget_black):
        log = Log()
        log.set_logger(run.get_device()['model'], os.path.join(run.get_path(), 'client.log'))
        log.i('udid: %s', run.get_device()['udid'])

        # set cls.path, it must be call before operate on any page
        path = ReportPath()
        path.set_path(run.get_path())

        # set cls.driver, it must be call before operate on any page
        base_page = BasePage()
        if 'ip' in run.get_device():
            base_page.set_driver(run.get_device()['ip'])
        else:
            base_page.set_driver(run.get_device()['serial'])

        try:
            # run cases
            base_page.d.shell('logcat -c')  # 清空logcat
            if cases:
                run.run_cases(cases)

            Maxim().run_monkey(monkey_shell=command, actions=actions, widget_black=widget_black)
            base_page.d.shell('logcat -d > /sdcard/logcat.log')
            time.sleep(1)

            base_page.d.pull('/sdcard/logcat.log', os.path.join(path.get_path(), 'logcat.log'))
            base_page.d.pull('/sdcard/monkeyerr.txt', os.path.join(path.get_path(), 'monkeyerr.txt'))
            base_page.d.pull('/sdcard/monkeyout.txt', os.path.join(path.get_path(), 'monkeyout.txt'))

            base_page.set_original_ime()
            base_page.identify()
            if 'ip' in run.get_device():
                log.i('release device %s ' % run.get_device()['serial'])
                atxserver2().release_device(run.get_device()['serial'])

        except AssertionError as e:
            log.e('AssertionError, %s', e)

    def run(self, devices, cases, apk_info, retry=3, save_last_try=True):
        if not devices:
            logger.error('There is no device found,test over.')
            return
        logger.info('Starting Run test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        runs = []
        for i in range(len(devices)):
            runs.append(RunCases(devices[i], apk_info['folder']))

        # run on every device 开始执行测试
        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_cases,
                             args=(run, cases, retry, save_last_try))
            time.sleep(2)
        logger.info('Waiting for all runs done........ ')
        pool.close()
        time.sleep(1)
        pool.join()
        logger.info('All runs done........ ')

        #  Generate statistics report  生成统计测试报告 将所有设备的报告在一个HTML中展示
        build_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        title = '报告生成时间: %s<br />测试包地址： <a href="%s">%s</a>' \
                '<br />PackageName: %s<br /> Version: %s<br />VersionCode: %s' % (
                    build_time, apk_info['url'], apk_info['url'], apk_info["package"], apk_info["versionName"],
                    apk_info["versionCode"])

        create_statistics_report(runs, title=title, sreport_path=apk_info['folder'])

    def run_maxim(self, cases=None, command=None, actions=False, widget_black=False):
        # start_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        devices = check_devives()
        if not devices:
            print('There is no device found,test over.')
            return
        print('Starting Run test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        runs = []
        for i in range(len(devices)):
            runs.append(RunMaxim(devices[i]))

        # run on every device 开始执行测试
        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_maxim,
                             args=(run, cases, command, actions, widget_black))
        print('Waiting for all runs done........ ')
        pool.close()
        pool.join()
        print('All runs done........ ')

    def run_single_case(self, cases=None):
        # start_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        devices = check_devives()
        if not devices:
            print('There is no device found,test over.')
            return
        print('Starting Run test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        runs = []
        for i in range(len(devices)):
            runs.append(RunMaxim(devices[i]))

        # run on every device 开始执行测试
        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_single_case, args=(run, cases))
        print('Waiting for all runs done........ ')
        pool.close()
        pool.join()
        print('All runs done........ ')

    @staticmethod
    def _run_single_case(run, cases):
        log = Log()
        log.set_logger(run.get_device()['model'], os.path.join(run.get_path(), 'client.log'))
        log.i('udid: %s', run.get_device()['udid'])

        # set cls.path, it must be call before operate on any page
        path = ReportPath()
        path.set_path(run.get_path())

        # set cls.driver, it must be call before operate on any page
        base_page = BasePage()
        if 'ip' in run.get_device():
            base_page.set_driver(run.get_device()['ip'])
        else:
            base_page.set_driver(run.get_device()['serial'])

        try:
            # run cases
            base_page.d.shell('logcat -c')  # 清空logcat
            if cases:
                run.run_cases(cases)
            base_page.set_original_ime()
            base_page.identify()
            if 'ip' in run.get_device():
                log.i('release device %s ' % run.get_device()['serial'])
                atxserver2().release_device(run.get_device()['serial'])
        except AssertionError as e:
            log.e('AssertionError, %s', e)

    @staticmethod
    def _run_solox_android(package=None, deviceId=None, duration=60):
        try:
            apm = APM(pkgName=package, platform='Android', deviceId=deviceId,
                      surfaceview=True, noLog=False, pid=None, duration=duration, record=False)
            apm.collectAll()  # will generate HTML report
        except Exception as e:
            traceback.format_exc()
            log.e(f"Device: {deviceId} excute fail !!!")

    def run_solox_android(self, package=None, duration=60):
        """
        param:package:包名,duration:执行时长，单位s
        """
        d = Devices()
        deviceIds = d.getDeviceIds()
        if not deviceIds:
            print('There is no device found,test over.')
            return
        print('Starting Run solox >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # self._run_solox_android(package, deviceIds[0], duration)
        # run on every device 开始执行测试
        pool = ThreadPool(len(deviceIds))
        # pool = Pool(processes=len(deviceIds))
        for runId in deviceIds:
            print(f'Device for {runId} is running........ ')
            pool.apply_async(self._run_solox_android,
                             args=(package, runId, duration))
        print('Waiting for all runs done........ ')
        pool.close()
        pool.join()
        print('All runs done........ ')
        print('Ending Run solox >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    def run_maxim(self, cases=None, command=None, actions=False, widget_black=False):
        # start_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        devices = check_devives()
        if not devices:
            print('There is no device found,test over.')
            return
        print('Starting Run test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        runs = []
        for i in range(len(devices)):
            runs.append(RunMaxim(devices[i]))

        # run on every device 开始执行测试
        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_maxim,
                             args=(run, cases, command, actions, widget_black))
        print('Waiting for all runs done........ ')
        pool.close()
        pool.join()
        print('All runs done........ ')

    def run_twmonkey(self, cases=None, command=None, excute_time=None):
        # start_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        devices = check_devives()
        if not devices:
            print('There is no device found,test over.')
            return
        print('Starting Run twmonkey test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        runs = []
        for i in range(len(devices)):
            runs.append(RunTWmonkey(devices[i]), 'TWmonkeyReport')

        # run on every device 开始执行测试
        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_twmonkey,
                             args=(run, cases, command, excute_time))
        print('Waiting for all twmonkey runs done........ ')
        pool.close()
        pool.join()
        print('All twmonkey runs done........ ')

    @staticmethod
    def _run_twmonkey(run, cases, command, excute_time):
        log = Log()
        log.set_logger(run.get_device()['model'], os.path.join(run.get_path(), 'client.log'))
        log.i('udid: %s', run.get_device()['udid'])

        # set cls.path, it must be call before operate on any page
        path = ReportPath()
        path.set_path(run.get_path())

        # set cls.driver, it must be call before operate on any page
        base_page = BasePage()
        if 'ip' in run.get_device():
            base_page.set_driver(run.get_device()['ip'])
        else:
            base_page.set_driver(run.get_device()['serial'])

        try:
            # run cases
            base_page.d.shell('logcat -c')  # 清空logcat
            if cases:
                run.run_cases(cases)
            TWMonkey().run_monkey(monkey_shell=command, excute_time=excute_time)

            base_page.d.shell('logcat -d > /sdcard/logcat.log')
            time.sleep(1)

            base_page.d.pull('/sdcard/logcat.log', os.path.join(path.get_path(), 'logcat.log'))
            base_page.d.pull('/sdcard/monkeyerr.txt', os.path.join(path.get_path(), 'monkeyerr.txt'))
            base_page.d.pull('/sdcard/monkeyout.txt', os.path.join(path.get_path(), 'monkeyout.txt'))

            base_page.set_original_ime()
            base_page.identify()
            if 'ip' in run.get_device():
                log.i('release device %s ' % run.get_device()['serial'])
                atxserver2().release_device(run.get_device()['serial'])

        except AssertionError as e:
            log.e('AssertionError, %s', e)

    @staticmethod
    def _run_fastbot(run, cases, command, actions, widget_black):
        log = Log()
        log.set_logger(run.get_device()['model'], os.path.join(run.get_path(), 'client.log'))
        log.i('udid: %s', run.get_device()['udid'])

        # set cls.path, it must be call before operate on any page
        path = ReportPath()
        path.set_path(run.get_path())

        # set cls.driver, it must be call before operate on any page
        base_page = BasePage()
        if 'ip' in run.get_device():
            base_page.set_driver(run.get_device()['ip'])
        else:
            base_page.set_driver(run.get_device()['serial'])

        try:
            # run cases
            base_page.d.shell('logcat -c')  # 清空logcat
            if cases:
                run.run_cases(cases)
            TWfastBot().run_monkey(monkey_shell=command, actions=actions, widget_black=widget_black)

            base_page.d.shell('logcat -d > /sdcard/logcat.log')
            time.sleep(1)
            base_page.d.pull('/sdcard/logcat.log', os.path.join(path.get_path(), 'logcat.log'))
            base_page.d.pull('/sdcard/monkeyerr.txt', os.path.join(path.get_path(), 'monkeyerr.txt'))
            base_page.d.pull('/sdcard/monkeyout.txt', os.path.join(path.get_path(), 'monkeyout.txt'))

            base_page.set_original_ime()
            base_page.identify()
            if 'ip' in run.get_device():
                log.i('release device %s ' % run.get_device()['serial'])
                atxserver2().release_device(run.get_device()['serial'])

        except AssertionError as e:
            log.e('AssertionError, %s', e)

    def run_fastbot(self, cases=None, command=None, actions=False, widget_black=False):
        devices = check_devives()
        if not devices:
            print('There is no device found,test over.')
            return
        print('Starting Run fastbot >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        runs = []
        for i in range(len(devices)):
            runs.append(RunTWmonkey(devices[i], 'FastbotReport'))

        # run on every device 开始执行测试
        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_fastbot,
                             args=(run, cases, command, actions, widget_black))
        print('Waiting for all fastbot runs done........ ')
        pool.close()
        pool.join()
        print('All runs fastbot done........ ')
