# coding=utf-8
from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import json
import os

import util
import config


class Douyu(QThread):
	log_text_send = pyqtSignal(str)
	
	def __init__(self, has_login=False):
		super().__init__()
		self.init_url = "https://www.douyu.com/directory/myFollow"
		self.base_url = "https://www.douyu.com"
		
		self.xpath_input = '//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/textarea'
		self.xpath_send = '//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/div[2]'
		
		self._chrome_options = webdriver.ChromeOptions()
		self._chrome_options.add_argument('--headless')
		if not has_login:
			self.browser = webdriver.Chrome()
		else:
			# chrome_options=self._chrome_options
			self.browser = webdriver.Chrome()
	
	def login(self, platform):
		if os.path.exists(config.cookies_path):
			self.init_cookies(platform)
		# self.browser.get(self.init_url)
		# self.browser.add_cookie(self.get_cookies(platform))
		else:
			self.init_cookies(platform)
	
	def get_cookies(self, platform):
		try:
			cookies = util.read_json_file(file_path=config.cookies_path)[platform]
			return cookies
		except KeyError or FileNotFoundError:
			self.log_text_send.emit("get cookies error")
			print("get cookies error")
			return
	
	def init_cookies(self, platform):
		
		xpath_login = '//*[@id="js-header"]/div/div/div[3]/div[7]/div/div/a/span'
		xpath_player = '//*[@id="js-header"]/div/div/div[3]/div[7]/div/a/span/div/div/img'
		self.browser.get(url=self.init_url)
		self.browser.maximize_window()
		
		time.sleep(2)
		self.log_text_send.emit(self.browser.current_url)
		
		if util.find_xpath_in_xml(self.browser, xpath_login):
			self.browser.find_element_by_xpath(xpath=xpath_login).click()
			
			if util.find_xpath_in_xml(self.browser, xpath_player):
				util.write_json_file(file_path=config.cookies_path, data={platform: self.browser.get_cookies()[0]})
			# self.browser.close()
			# chrome_options=self._chrome_options
			# self.browser = webdriver.Chrome()
			
			# self.login(platform)
	
	def send_msg(self, room, msg):
		
		self.login("douyu")
		url = "%s/%s" % (self.base_url, str(room))
		self.browser.get(url)
		self.browser.maximize_window()
		xpath_top_line = '//*[@id="js-player-title"]/div/div[3]/div[1]'
		if not util.find_xpath_in_xml(self.browser, xpath_top_line):
			return
		top_line = self.browser.find_element_by_xpath(xpath_top_line)
		
		self.browser.execute_script("arguments[0].scrollIntoView();", top_line)
		if util.find_xpath_in_xml(self.browser, self.xpath_input):
			input_msg = self.browser.find_element_by_xpath(self.xpath_input)
			input_msg.click()
			time.sleep(1)
			input_msg.send_keys(msg)
			time.sleep(1)
			if util.find_xpath_in_xml(self.browser, self.xpath_send):
				self.browser.find_element_by_xpath(self.xpath_send).click()
				return True
			else:
				print("send msg failed")
				return False
		else:
			print("send msg failed")
			return False


if __name__ == '__main__':
	D = Douyu()
	# D.login("douyu")
	D.send_msg(6326110, "66666")
	
	# D.browser.close()
