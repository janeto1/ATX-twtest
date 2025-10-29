import time

import uiautomator2 as u2

d = u2.connect_usb("PQY0220C04031161")
# 亮屏
# d.screen_on()
# d.session("com.agentplusstudio")
d.app_start("com.taiwu.find")
# d.implicitly_wait(5)
# d.click(0.316, 0.337)
# d.clear_text()
# d(resourceId='RNE__Input__text-input', text='请输入域帐号').set_text("yangpeng8")
# d.click(0.316, 0.408)
# d.clear_text()
# d(resourceId='RNE__Input__text-input', text='请输入密码').set_text("test.1234")
# d(className='android.widget.TextView', text='登录').click()
# time.sleep(2)
# d(className='android.widget.TextView', text='房源').click()
# d.click(0.29, 0.973)
# d.shell('mkdir -p /sdcard/max-output/20230818153542/')
# d.shell('/sdcard/max-output/20230818153542/monkeyout.txt')
# d.shell('/sdcard/max-output/20230818153542/monkeyerr.txt')
# d.pull('/sdcard/max-output/20230818153542/monkeyout.txt', 'D:/code/ATX-Test/log/1233334.txt')
commond = "CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/fastbot-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey -p com.taiwu.find --agent reuseq --act-whitelist-file /sdcard/awl.strings --running-minutes 1 --throttle 500  -v -v  >/sdcard/monkeyout.txt 2>/sdcard/monkeyerr.txt &"
output, exit_code = d.shell(commond)
# output, exit_code = d.shell("ps -A", timeout=60)
print(output)
# for i in range(50):
#     d.drag(0.584, 0.264, 0.599, 0.629)
#
# print(d.info)
