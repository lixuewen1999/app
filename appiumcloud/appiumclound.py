'''
@author: lixuewen
@file: appiumclound.py
@time: 2020/9/23 14:04
@desc: 云测试平台
'''
import socket,os,subprocess,threading
from appium import webdriver
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class AppiumCloud:
    def __init__(self):
        pass

    def build_devices(self):
        list = []
        port = 5000
        bport = 8000
        devices = subprocess.check_output('adb devices').decode().strip().split('\r\n')
        for i in range(1,len(devices)):
            udid = devices[i].split('\t')[0]
            if udid != '':
                dic = {}
                version = subprocess.check_output('adb -s {} shell getprop ro.build.version.release'.format(udid)).decode().strip()
                port = self.find_port(port)
                bport = self.find_port(bport)
                dic['udid'] = udid
                dic['port'] = port
                dic['bport'] = bport
                dic['version'] = version
                list.append(dic)
                port += 1
                bport += 1
        return list

    def find_port(self,port):
        while True:
            if self.check_port(port):
                break
            else:
                port += 1
        return port

    def check_port(self,port):
        s = socket.socket()
        try:
            s.connect(('127.0.0.1',port))
            return False
        except:
            return True


    def start_appium(self,port,bport,udid,version):
        log_file = os.path.abspath('.')+'\log\{}'.format(udid.replace(':','_'))
        cmd = r'start /b appium -a 127.0.0.1 -p {} -bp {} --udid {} --platform-version {} --log {} --log-level info --log-timestamp'.format(port,bport,udid,version,log_file)
        print(cmd)
        os.system(cmd)
        self.test(udid,version,port)

    def test(self,udid,version,port):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = version
        desired_caps['deviceName'] = 'Appium'
        desired_caps['noReset'] = True
        desired_caps['appPackage'] = 'com.miui.calculator'
        desired_caps['appActivity'] = '.cal.CalculatorActivity'
        desired_caps['udid'] = udid
        desired_caps['unicodekeyboard'] = True
        driver = webdriver.Remote('http://127.0.0.1:{}/wd/hub'.format(port),desired_caps)
        driver.find_element_by_id('com.miui.calculator:id/btn_1_s').click()
        driver.find_element_by_id('com.miui.calculator:id/btn_plus_s').click()
        driver.find_element_by_id('com.miui.calculator:id/btn_1_s').click()
        driver.find_element_by_id('com.miui.calculator:id/btn_equal_s').click()
        result = WebDriverWait(driver,10, 0.5).until(EC.presence_of_element_located((By.ID,'com.miui.calculator:id/result')))
        if result.get_attribute('text') == '= 2':
            print('pass')
        else:
            print('fail')


if __name__ == '__main__':
    os.system('taskkill /IM node.exe /F')
    ac = AppiumCloud()
    devices = ac.build_devices()
    print(devices)
    for i in devices:
        threading.Thread(target=ac.start_appium,args=(i['port'],i['bport'],i['udid'],i['version'])).start()