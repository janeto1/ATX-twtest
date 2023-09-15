#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Public.decorator import *
import unittest

from Demo.Page import login_user
from Demo.Page import login

apk_path = r'E:/app/user/2023-08-04/taiwu_4.0.8_release_07-25_encrypted_taiwu_4.apk'


# pkg_name = 'com.agentplusstudio'


class abcd(unittest.TestCase, BasePage):
    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.app_stop_all()

    @testcase
    def test_login_user(self, ):
        """
        登录用户空间
        """
        '''安装启动android_app_bootstrap'''
        pkg_name = 'com.taiwu.find'
        # self.d.app_uninstall(pkg_name)
        # self.local_install(apk_path)
        self.d.app_start(pkg_name)
        self.set_fastinput_ime()
        time.sleep(3)
        login_user.login_user().hot_login()

    @testcase
    def test_install_login(self, ):
        """
        登录经纪人空间
        """
        # self.d.app_uninstall(pkg_name)
        # self.local_install(apk_path)
        pkg_name = "com.agentplusstudio"
        self.d.app_start(pkg_name)
        self.set_fastinput_ime()
        time.sleep(3)
        login.login_page().input_username('yangpeng8')
        login.login_page().input_password('test.1234')
        login.login_page().click_login_btn()

    @testcase
    def test_solopi(self, ):
        pkg_name = 'com.alipay.hulu'
        self.d.app_stop(pkg_name)
        self.d.app_start(pkg_name)
        time.sleep(3)
        login_user.login_user().solopi_agreement()
        login_user.login_user().solopi_stress()
        login_user.login_user().solopi_upmonitor()
        login_user.login_user().solopi_battary()
        login_user.login_user().solopi_cpu()
        login_user.login_user().solopi_fps()
        login_user.login_user().solopi_memory()
        login_user.login_user().solopi_network()
        login_user.login_user().solopi_tempate()
        login_user.login_user().solopi_record()


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    cases = unittest.TestSuite()
    cases.addTest(abcd('test_install_login'))
    runner.run(cases)
