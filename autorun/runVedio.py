#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uiautomator2 as u2
import time

# 连接设备
d = u2.connect("PQY0220C04031161")

# 进入视频页面
d(text="二手房").click()
time.sleep(1)
d(text="切到视频").click()
time.sleep(60)
d(text="花木苑").click()

print("已进入【花木苑】视频，开始播放第一个视频...")

# 获取屏幕尺寸
w, h = d.window_size()
print(f"屏幕分辨率: {w} x {h}")

# 滑动持续时间（秒）
SWIPE_DURATION = 0.8

# 向上滑动（下一个视频）
def swipe_up():
    d.swipe(w * 0.5, h * 0.7, w * 0.5, h * 0.3, SWIPE_DURATION)
    time.sleep(3)  # 等待视频加载

# 向下滑动（上一个视频）
def swipe_down():
    d.swipe(w * 0.5, h * 0.3, w * 0.5, h * 0.7, SWIPE_DURATION)
    time.sleep(3)  # 等待视频加载

# ================================
# 第1步：播放第一个视频 2 分钟
# ================================
print("【视频 1/21】正在播放第一个视频...")
time.sleep(120)

# ================================
# 第2步：向上滑动 10 次，每次播放 2 分钟
# ================================
for i in range(1, 11):
    print(f"【视频 {i+1}/21】向上滑动 → 第 {i+1} 个视频，播放 2 分钟...")
    swipe_up()
    time.sleep(120)  # 每个视频播放 2 分钟

# ================================
# 第3步：向下滑动 10 次，每次播放 2 分钟
# ================================
for i in range(10):
    print(f"【视频 {11+i+1}/21】向下滑动 → 第 {11+i+1} 个视频，播放 2 分钟...")
    swipe_down()
    time.sleep(120)  # 每个视频播放 2 分钟

print("✅ 所有 21 个视频播放完成，自动化任务结束！")