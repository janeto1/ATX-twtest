from Monitor.solox_run import excute_solox
import sys

if __name__ == '__main__':
    package = 'com.taiwu.find'
    soloxTime = 120  # 秒

    # 打开本地监控solox
    if len(sys.argv) > 1:
        soloxTime = sys.argv[1]
        print(f"系统参数值为{sys.argv[1]}")
    excute_solox(package=package, soloxTime=soloxTime)
