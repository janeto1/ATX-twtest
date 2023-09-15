#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from Public.basepage import BasePage
# from uiautomator2 import UiObjectNotFoundError
from Public.decorator import *
from Public.log import Log
from Demo import dm_config
import json
from Public.filetools import read_file

log = Log()

"""
用户空间登录页
"""


class login_user(BasePage):

    @teststep
    def confirm_agreement(self, ):
        log.i('首次加载协议')
        if self.d(text='同意并继续使用APP').exists(timeout=3):
            self.d(text='同意并继续使用APP').click()
        # watcher = self.watch_device("同意并继续使用APP")
        # self.unwatch_device(watcher)

    @teststep
    def wait_page(self, text):
        if self.d(text=text).wait(timeout=3):
            return True
        else:
            return False

    @teststep
    def click_buttom_menu(self, text):
        """
        点击主页底部菜单
        """
        log.i('点击底部菜单:%s' % text)
        self.d(className="android.widget.TextView", text=text, index=2).click(timeout=3)

    @teststep
    def hot_login(self, ):
        """
        本机一键登录
        """
        is_home = self.wait_page("首页")
        # 加载协议
        if not is_home:
            self.confirm_agreement()
        self.click_buttom_menu("我")
        # 是否登录
        is_login = self.wait_page("登录/注册")
        if is_login:
            self.d(text="登录/注册", className="android.widget.TextView").click(timeout=3)
            self.d(className="android.widget.CheckBox").click(timeout=3)
            self.d(text="一键登录").click(timeout=3)

    @teststep
    def solopi_agreement(self, ):
        log.i('同意solopi运行协议')
        path = '//*[@resource-id="android:id/button1"]'
        try:
            if self.wait_element(self.d.xpath(path), times=3):
                self.d.xpath(path).click_exists(timeout=3)
        except Exception as e:
            log.e('元素识别失败: 同意solopi运行协议')

    @teststep
    def solopi_stress(self, ):
        log.i('选择solopi性能测试')
        try:
            if self.wait_element(self.d(text="性能测试", resourceId="com.alipay.hulu:id/tv")):
                self.d(text="性能测试", resourceId="com.alipay.hulu:id/tv").click(timeout=3)
        except Exception as e:
            log.e('元素识别失败: 选择solopi性能测试')

    @teststep
    def solopi_battary(self, ):
        log.i('选择solopi监控: 电池')
        path = '//*[@resource-id="com.alipay.hulu:id/perform_float_list"]/android.widget.LinearLayout[1]/android.widget.CheckBox[1]'
        try:
            if self.wait_element(self.d.xpath(path)):
                self.d.xpath(path).click_exists(timeout=3)
        except Exception as e:
            log.e('元素识别失败: 选择solopi监控: 电池')

    @teststep
    def solopi_cpu(self, ):
        log.i('选择solopi监控: cpu')
        path = '//*[@resource-id="com.alipay.hulu:id/perform_float_list"]/android.widget.LinearLayout[2]/android.widget.CheckBox[1]'
        try:
            if self.wait_element(self.d.xpath(path)):
                self.d.xpath(path).click_exists(timeout=3)
        except Exception as e:
            log.e('元素识别失败: 选择solopi监控: cpu')

    @teststep
    def solopi_fps(self, ):
        log.i('选择solopi监控: fps帧率')
        path1 = '//*[@resource-id="com.alipay.hulu:id/perform_float_list"]/android.widget.LinearLayout[3]/android.widget.CheckBox[1]'
        path2 = '//*[@text="我知道了"]'
        try:
            if self.wait_element(self.d.xpath(path1)):
                self.d.xpath(path1).click_exists(timeout=3)

            if self.wait_element(self.d.xpath(path2)):
                self.d.xpath(path2).click(timeout=3)
        except Exception as e:
            log.e('元素识别失败: 选择solopi监控: fps帧率')

    @teststep
    def solopi_memory(self, ):
        log.i('选择solopi监控: 内存')
        path = '//*[@resource-id="com.alipay.hulu:id/perform_float_list"]/android.widget.LinearLayout[5]/android.widget.CheckBox[1]'
        try:
            if self.wait_element(self.d.xpath(path)):
                self.d.xpath(path).click_exists(timeout=3)
        except Exception as e:
            log.e('元素识别失败: 选择solopi监控: 内存')

    @teststep
    def solopi_network(self, ):
        log.i('选择solopi监控: 网络')
        path = '//*[@resource-id="com.alipay.hulu:id/perform_float_list"]/android.widget.LinearLayout[3]/android.widget.CheckBox[1]'
        try:
            if self.wait_element(self.d.xpath(path)):
                self.d.xpath(path).click_exists(timeout=3)
        except Exception as e:
            log.e('元素识别失败: 选择solopi监控: 网络')

    @teststep
    def solopi_tempate(self, ):
        log.i('选择solopi监控: 温度')
        path = '//*[@resource-id="com.alipay.hulu:id/perform_float_list"]/android.widget.LinearLayout[9]/android.widget.CheckBox[1]'
        try:
            if self.wait_element(self.d.xpath(path)):
                self.d.xpath(path).click_exists(timeout=3)
        except Exception as e:
            log.e('元素识别失败: 选择solopi监控: 温度')

    @teststep
    def solopi_upmonitor(self, ):
        log.i('选择solopi监控: 收起监控')
        path = '//*[@resource-id="com.alipay.hulu:id/float_stress_hide"]'
        try:
            if self.wait_element(self.d.xpath(path)):
                self.d.xpath(path).click_exists(timeout=3)
        except Exception as e:
            log.e('元素识别失败: 选择solopi监控: 收起监控')

    @teststep
    def solopi_record(self, ):
        log.i('选择solopi监控: 开始执行监控')
        path = '//*[@resource-id="com.alipay.hulu:id/recordIcon"]'
        try:
            if self.wait_element(self.d.xpath(path)):
                self.d.xpath(path).click_exists(timeout=3)
        except Exception as e:
            log.e('元素识别失败: 选择solopi监控: 开始执行监控')
