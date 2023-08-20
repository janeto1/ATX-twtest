#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import base64
import whichcraft

# atxserver2 地址及token
SERVER = 'http://10.0.32.80:4000'
token = '8199a587ce0744f0bf99e34e2085f51d'

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(current_path)
bundle_tool_path = os.path.join(current_path, 'static', 'bundletool-all.jar')
tmp_apks_path = os.path.join(current_path, 'tmp.apks')
ks_path = os.path.join(current_path, 'static', 'ksfile')
maxin_path = os.path.join(current_path, 'Maxim')

unlock_apk = os.path.join(current_path, 'static', 'unlock.apk')
test_apk = os.path.join(current_path, 'static', 'android_app_bootstrap-debug.apk')
local_log_path = os.path.join(parent_path, 'log')

# dic internalapp
# key: packagename
# name: app名称
# app_folder: app在手机上可能存在的文件夹路径
internalapp = \
    {
        "com.quvideo.xiaoying":
            {"name": "小影App",
             "app_folder": ["/sdcard/DCIM/XiaoYing", "/sdcard/XiaoYing", "/sdcard/DCIM/GIF", "/sdcard/DCIM/Giphy"]
             },
    }

brand_filemanager = \
    {'HUAWEI': 'com.huawei.hidisk',
     'Xiaomi': 'com.android.fileexplorer',
     'vivo': 'com.android.filemanager',
     'Lenovo': 'com.zui.filemanager',
     'SMARTISAN': 'com.smartisanos.filemanager',
     'nubia': 'cn.nubia.myfile',
     'Nokia': 'com.nbc.filemanager',
     'OPPO': 'com.coloros.filemanager',
     'Meizu': 'com.meizu.filemanager',
     'samsung': 'com.sec.android.app.myfiles',
     'OnePlus': 'com.oneplus.filemanager',
     }


def get_ks_info(ks_path):
    '''
    获取ks信息
    :return: [ks_pass, key_alias, key_pass]
    '''

    return None


def get_java_path():
    global jpath
    if whichcraft.which('java'):
        jpath = whichcraft.which('java')
    else:
        raise Exception('Java 环境配置异常 请检查电脑Java环境配置')
    return jpath


def build_apks_code(bundle_path=None, ks_path=None, apks_path=None):
    ks_info = get_ks_info(ks_path)
    code = '%s -jar %s build-apks --bundle=%s --output=%s --overwrite --ks=%s ' \
           '--ks-pass=pass:%s --ks-key-alias=%s --key-pass=pass:%s --mode=universal' % \
           (get_java_path(), bundle_tool_path, bundle_path, apks_path, ks_path, ks_info[0], ks_info[1],
            ks_info[2])
    return code.split(' ')


def ensure_path(path: str) -> str:
    """
    兼容不同系统路径
    :param path:
    :return:
    """
    if "/" in path:
        path = os.sep.join(path.split("/"))
    if "\\" in path:
        path = os.sep.join(path.split("\\"))
    file_path = os.path.join(local_log_path, path)
    create_dir(file_path)
    return file_path.replace('\\', '/')


def create_dir(file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)


def create_file(file_name):
    if not os.path.exists(file_name):
        open(file_name, 'w').close()
