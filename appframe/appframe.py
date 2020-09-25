'''
@author: lixuewen
@file: appframe.py
@time: 2020/9/23 17:36
@desc: 基于app的兼容性测试框架
'''


import os,subprocess,time
from  time import sleep
class AppFrame:
    def __init__(self):
        self.app_list = []

    def install(self):
        apk_list = os.listdir('./app')
        for apk in apk_list:
            apk_path = os.path.abspath('./app')+'\\'+apk
            output = os.popen('aapt dump badging {} | findstr "package"'.format(apk_path)).read()
            package = output.split("'")[1]
            # output = os.popen('aapt dump badging {} | findstr "launchable activity"'.format(apk_path)).read().decode('utf-8')
            output = subprocess.check_output('aapt dump badging {} | findstr "launchable activity"'.format(apk_path)).decode()
            activity = output.split("'")[1]
            dic = {}
            dic['package'] = package
            dic['activity'] = activity
            self.app_list.append(dic)
            output = os.popen('adb install -r {}'.format(apk_path)).read()
            if 'Failure' in output:
                print('安装应用程序：{}，失败'.format(package))
                self.result(package,'安装应用','失败')
            elif 'Success' in output:
                print('安装应用程序：{}，成功'.format(package))
                self.result(package,'安装应用','成功')

    def run(self):
        for app in self.app_list:
            package = app['package']
            activity = app['activity']
            output = os.popen('adb shell am start -W -n {}/{}'.format(package,activity)).read()
            process = os.popen('adb shell ps | findstr "{}"'.format(package)).read()
            sleep(5)
            if package in process:
                print('启动应用程序:{},成功'.format(package))
                self.result(package,'启动应用','成功')
            else:
                print('启动应用程序:{},失败'.format(package))
                self.result(package,'启动应用','失败')

    def monkey(self):
        for app in self.app_list:
            package = app['package']
            log = os.path.abspath('./log')+'/moneky_{}'.format(package)
            os.system('adb shell monkey -p {} --throttle 100 50 > {}'.format(package,log))
            sleep(3)

    def uninstall(self):
        for app in self.app_list:
            output = os.popen('adb uninstall {}'.format(app['package'])).read()
            print(output)
            if 'Success' in output:
                print('卸载应用程序:{},成功'.format(app['package']))
                self.result(app['package'],'卸载应用','成功')
            else:
                print('卸载应用程序:{},失败'.format(app['package']))
                self.result(app['package'],'卸载应用','失败')



    def result(self,package,type,result):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        with open('./result/result.csv','a+',encoding='utf-8') as file:
            file.write('{},{},{},{}\n'.format(now,package,type,result))




if __name__ == '__main__':
    app = AppFrame()
    app.install()
    app.run()
    app.monkey()
    app.uninstall()