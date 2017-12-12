#!/usr/bin/python
# -*-coding:-utf-8-*-
import os
import urllib
import commands
import time
import socket



# 定义变量
dtNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

appName = 'automator'


#pidSh = "ps -ef|grep " + appName +" | grep -v '/grep " + appName +" '/ | awk '{print $2}'"
#pid = pid = commands.getoutput(pidSh)


acHome = "/home/tomcat/release/automator/"
# 启动应用的脚本，要求写绝对路径
startSh = acHome + "start.sh"


checkURL = "http://127.0.0.1:2222/health"
otcCountURL = "https://otc.forotc.com/robot/getRobotAdClosedCount"


# 设置超时时间
socket.setdefaulttimeout(20)

catId = "cat '" + acHome + appName + ".pid" + "'"
print catId


def get_pid():
    rtn = commands.getoutput(catId)
    if rtn.isdigit():
        return rtn
    else:
        return 0


def reboot_process(pid, start_sh):
    if not start_sh:
        print("start_sh must not be null")
        return
    if get_pid():
        print dtNow, "kill pid " + pid
        os.system("kill " + pid)
        os.system("kill -9 " + pid)
        time.sleep(2)
    os.system(start_sh)


def send_get_request(url):
    pass


def check_robot_alive():

    print ("------------- check robot alive ---------------")
    print dtNow, "开始检查 robot..."
    if get_pid():
        print dtNow, "进程已存在，检测health url是否正常..."
        try:
            response_code = urllib.urlopen(checkURL).getcode()
            if response_code == 200:
                print dtNow, "URL可以正常访问，无需重启robot."
            else:
                print dtNow, "页面访问出错,开始重启robot."
                reboot_process(get_pid(), startSh)
        except Exception, e:
            print "type(e)=%s" % type(e)
            print(dtNow, "无法访问到health, 准备重启动robot... ")
            reboot_process(get_pid(), startSh)
    else:
        pass
        print dtNow, "进程不存在，准备启动robot... "
        os.system(startSh)


def check_closed_ad_per_15_min():
    print ("-------------- get count from otc --------------")
    response = urllib.urlopen(otcCountURL).read()
    print("All robot close ad count:" + response)
    if int(response) < 15:
        print("12分钟内取得的数据小于15，正在重启robot服务器...")
        reboot_process(get_pid(), startSh)
    else:
        print("Status OK... ")


while True:
    time.sleep(2)
    check_robot_alive()
    #check_closed_ad_per_15_min()
