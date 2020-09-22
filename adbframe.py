'''
@author: lixuewen
@file: adbframe.py
@time: 2020/9/22 18:46
@desc: 基于adb命令的移动端测试框架
'''
import os
from lxml import etree
class adbframe:

    def __init__(self,package,activity,path=r'E:\Android'):
        self.x = 0
        self.y = 0
        self.path = path
        self.attrs = None
        self.start_app(package,activity)

    def get_xml(self,xml_path=r'/storage/emulated/legacy/window_dump.xml'):
        os.system('adb shell uiautomator dump')
        os.system('adb pull {} {}'.format(xml_path,self.path))

    def find_xpath(self,xpath):
        self.get_xml()
        tree = etree.parse('{}/window_dump.xml'.format(self.path))
        list = tree.xpath(xpath)
        self.attrs = list[0]
        self.get_coord(list[0].get('bounds'))
        return self

    def find_id(self,id):
        self.get_xml()
        tree = etree.parse('{}/window_dump.xml'.format(self.path))
        list = tree.xpath("/de[@resouce-id='%s']"%id)
        self.attrs = list[0]
        self.get_coord(list[0].get('bounds'))
        return self

    def find_content_desc(self,content_desc):
        self.get_xml()
        tree = etree.parse('{}/window_dump.xml'.format(self.path))
        list = tree.xpath("/de[content-desc='%s'']"%content_desc)
        self.attrs = list[0]
        self.get_coord(list[0].get('bounds'))
        return self

    def get_coord(self,str):
        str = str.replace('][',',')
        str = str.replace('[','')
        str = str.replace(']','')
        str_list = str.split(',')
        x = (int(str_list[0]) + int(str_list[2])) / 2
        y = (int(str_list[1]) + int(str_list[3])) / 2
        self.x = x
        self.y = y

    def clikc(self):
        os.system('adb shell input tap {} {}'.format(self.x,self.y))

    def send_keys(self,content):
        self.clikc()
        os.system('adb shell input text {}'.format(content))

    def start_app(self,package,activity):
        os.system('adb shell am start -n {}/{}'.format(package,activity))

    def assert_exist(self,xpath):
        try:
            self.find_xpath(xpath)
            print('pass')
        except:
            print('fail')

    def assert_equal(self,expect,actaul):
        if expect == actaul:
            print('pass')
        else:
            print('fail')

    def get_attribute(self,attr):
        return self.attrs.get(attr)



if __name__ == '__main__':
    adb = adbframe('com.miui.calculator','.cal.CalculatorActivity')
    adb.find_xpath('//node[@text="1"]').clikc()
    adb.find_xpath('//node[@resource-id="com.miui.calculator:id/btn_plus_s"]').clikc()
    adb.find_xpath('//node[@text="1"]').clikc()
    adb.find_xpath('//node[@resource-id="com.miui.calculator:id/btn_equal_s"]').clikc()
    actual = adb.find_xpath('//node[@resource-id="com.miui.calculator:id/result"]').get_attribute('text')
    adb.assert_equal('= 2',actual)




