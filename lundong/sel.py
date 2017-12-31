#!/usr/bin/python
#coding=utf-8

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

class my_sel():
    def __init__(self):
        self.Keys = Keys
        self.display = Display(visible=0,size=(800,600))
        self.display.start()
        self.driver = webdriver.PhantomJS(executable_path='phantomjs',service_log_path='/tmp/ghostdriver.log')
        self.driver.set_window_size(0,0)
        self.driver.set_page_load_timeout(30)
        self.wait = WebDriverWait(self.driver, 5)


    def isPrased(self,xpath):
        return EC.presence_of_element_located((By.XPATH, xpath))


    def get_xpath(self,xpath):
        self.wait.until(self.isPrased(xpath))
        return self.driver.find_element_by_xpath(xpath)

    def A_click(self,xpath):
        search_button_element = self.driver.find_element_by_xpath(xpath)
        ActionChains(self.driver).click(search_button_element).perform()

    def close(self):
        self.driver.quit()
        self.display.stop()

if __name__ == '__main__':
    sel = my_sel()
    sel.driver.get('http://www.baidu.com')
    print sel.driver.title
    sel.close()