#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from Public.basepage import BasePage
# from uiautomator2 import UiObjectNotFoundError
from Public.decorator import *
from Public.log import Log
from Demo import dm_config
import json
from Public.filetools import read_file

# package = json.loads(read_file(dm_config.info_path))['package']
log = Log()


class login_page(BasePage):
    @teststep
    def wait_page(self):
        if self.d(text="登录").wait(timeout=15):
            return True
        else:
            return False

    @teststep
    def input_username(self, text):
        log.i('输入用户名:%s' % text)
        self.d.click(0.327, 0.342)
        self.d.clear_text()
        self.d(resourceId="RNE__Input__text-input", text="请输入域帐号") \
            .set_text(text)

    @teststep
    def input_password(self, text):
        log.i('输入密码:%s' % text)
        self.d.click(0.477, 0.409)
        self.d.clear_text()
        self.d(resourceId="RNE__Input__text-input", text="请输入密码") \
            .set_text(text)

    @teststep
    def click_login_btn(self):
        log.i('点击登录按钮')
        self.d(className="android.widget.TextView", text="登录").click()
