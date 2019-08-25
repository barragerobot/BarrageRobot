# -*- coding: utf-8 -*-
from PIL import Image
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QGraphicsOpacityEffect, QPushButton
from logic import url_pool
import sys
import config
import time
import requests
import bs4
import traceback
import os


def get_log_str(msg: str):
	now_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	if len(config.log_text_str) > 5000:
		config.log_text_str = ""
	if config.log_text_str == "":
		config.log_text_str = now_time + " -> " + msg
	else:
		config.log_text_str = now_time + " -> " + msg + "\n" + config.log_text_str

	return config.log_text_str


class DouyuLogin(QThread):
	log_msg = pyqtSignal(str)
	is_finish = pyqtSignal(bool)

	def __init__(self):
		super().__init__(parent=None)

	def run(self):
		xpath_login_top = '//*[@id="js-header"]/div/div/div[3]/div[7]/div/div/a/span'


class RoomStatistics(QThread):
	sinOut = pyqtSignal(str)
	is_finish = pyqtSignal(bool)

	def __init__(self):
		super().__init__(parent=None)
		self.working = True

	def __del__(self):
		self.working = False

	def run(self):

		self.sinOut.emit(get_log_str("开始扫描斗鱼旗下所有分类列表,稍候........"))
		self.sinOut.emit(get_log_str("初始化"))
		url_pool.init_browser()
		self.sinOut.emit(get_log_str("初始化完成"))
		url_pool.get_douyu_directory()
		self.sinOut.emit(get_log_str("统计过程需要一些时间，不要着急，耐心等候....."))
		douyu_type_platform = url_pool.get_douyu_type_platform()
		self.sinOut.emit(get_log_str("斗鱼直播平台下的分类总数为 : %s" % len(douyu_type_platform)))

		for game_url in douyu_type_platform:
			time.sleep(config.request_wait_time)
			game_url_result = requests.get(game_url)
			if game_url_result.status_code == 200:
				self.sinOut.emit(get_log_str("网址为 %s 访问成功" % game_url))
			else:
				self.sinOut.emit(get_log_str("网址为 %s 访问失败" % game_url))
				continue
			soup_game = bs4.BeautifulSoup(game_url_result.text, "html.parser")

			game_room_list = soup_game.select(".layout-Cover-item")

			try:
				now_type_room_num = 0
				for game_room in game_room_list:
					room_url = "%s/%s" % (url_pool.douyu_base_url, game_room.select("a")[0].get("href"))
					url_pool.douyu_rooms.append(room_url)
					now_type_room_num += 1
				self.sinOut.emit(get_log_str("%s 下的房间数为 : %s" % (game_url, now_type_room_num)))
			except:
				self.sinOut.emit(get_log_str(traceback.print_exc()))

		self.sinOut.emit(get_log_str("开始扫描斗鱼旗下所有房间总数为 : %s" % len(url_pool.douyu_rooms)))
		self.is_finish.emit(True)

	def is_working(self):
		return self.working


class SendBarrage(QThread):
	sinOut = pyqtSignal(str)
	is_finish = pyqtSignal(bool)

	def __init__(self):
		super().__init__(parent=None)
		self.working = True
		self.chrome_browser = None

	def __del__(self):
		self.working = False

	@staticmethod
	def check_xpath(xpath, browser_object):
		count = 0
		while count < config.wait_time_max:
			count += 1
			try:
				browser_object.find_element_by_xpath(xpath)
				print("找到了")
				return True
			except:
				print("还没找到")
				time.sleep(1)
				continue
		return False

	def request_url(self, url, xpath):
		pass

	def login(self):
		xpath_login_top = '//*[@id="js-header"]/div/div/div[3]/div[7]/div/div/a/span'
		xpath_qr_code = '/html/body/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[1]/div/div[1]'
		self.sinOut.emit(get_log_str("二维码加载中"))
		self.chrome_browser.get('https://www.douyu.com')
		time.sleep(config.wait_time_max)
		self.chrome_browser.maximize_window()
		self.chrome_browser.set_page_load_timeout(config.wait_time_max)
		config.write_data("E:\\work_bill\\BarrageRobot\\resource\\11.html", self.chrome_browser.page_source)
		self.chrome_browser.find_element_by_xpath(xpath_login_top).click()
		self.chrome_browser.set_page_load_timeout(config.wait_time_max)
		time.sleep(config.wait_time_max)
		# self.chrome_browser.save_screenshot("E:\\work_bill\\BarrageRobot\\resource\\image\\scree.png")
		self.sinOut.emit(get_log_str("获得二维码"))

		imgelement = self.chrome_browser.find_element_by_xpath(xpath_qr_code)
		locations = imgelement.location
		sizes = imgelement.size
		rangle = (int(locations['x']), int(locations['y']), int(locations['x'] + sizes['width']),
				  int(locations['y'] + sizes['height']))
		path_1 = os.getcwd() + "\\resource\\image\\code_1.png"
		path_2 = os.getcwd() + "\\resource\\image\\code_2.png"
		self.chrome_browser.save_screenshot(path_1)
		img = Image.open(str(path_1) + ".png")

		jpg = img.crop(rangle)

		jpg.save(str(path_2) + ".png")

	def run(self):

		xpath_login_top = '//*[@id="js-header"]/div/div/div[3]/div[7]/div/div/a/span'
		xpath_login = '//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[3]/div[1]/span'
		xpath_input = '//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/textarea'
		xpath_send = '//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/div[2]'
		xpath_first_link = '//*[@id="js-header"]/div/div/div[1]/div/ul/li[1]/a'

		self.sinOut.emit(get_log_str("开始发送弹幕"))

		# chrome_options=chrome_options

		self.chrome_browser.get('https://www.douyu.com/101')

		try:
			time.sleep(config.wait_time_max)
			self.chrome_browser.maximize_window()
			self.chrome_browser.set_page_load_timeout(config.wait_time_max)
			config.write_data("E:\\work_bill\\BarrageRobot\\resource\\11.html", self.chrome_browser.page_source)
			self.chrome_browser.find_element_by_xpath(xpath_login_top).click()
			self.chrome_browser.set_page_load_timeout(config.wait_time_max)
			time.sleep(config.wait_time_max)

			self.chrome_browser.save_screenshot("E:\\work_bill\\BarrageRobot\\resource\\image\\scree.png")

			self.chrome_browser.get("https://www.douyu.com/101")
			url_pool.douyu_cookies = self.chrome_browser.get_cookies()
			print(url_pool.douyu_cookies)
		except:
			traceback.print_exc()

		self.is_finish.emit(True)

	def is_working(self):
		return self.working


class ViewMain(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle(config.view_title)
		self.resize(1200, 800)
		self.setMaximumSize(1200, 800)
		self.setMinimumSize(1200, 800)

		palette1 = QPalette()
		palette1.setColor(self.backgroundRole(), QColor(113, 175, 164))
		self.setPalette(palette1)

		self.log_browser = QTextBrowser(self)
		self.set_log_browser_style()

		self.btn_get_room_data = QPushButton("扫描房间", self)
		self.set_btn_get_room_data_style()

		self.btn_send_barrage = QPushButton("发送弹幕", self)
		self.set_btn_send_barrage()

		self.btn_login_douyu = QPushButton("登陆斗鱼", self)
		self.set_btn_login_douyu_style()

		self.btn_has_login_douyu = QPushButton("已经登陆斗鱼", self)
		self.set_btn_has_login_douyu_style()

		self.btn_login_huya = QPushButton("登陆虎牙", self)
		self.set_btn_login_huya_style()

		self.btn_has_login_huya = QPushButton("已经登陆虎牙", self)
		self.set_btn_has_login_huya_style()

		self.worker = RoomStatistics()
		self.worker.sinOut.connect(self.send_log)
		self.worker.is_finish.connect(self.check_finish)

		self.send_barrage = SendBarrage()
		self.send_barrage.sinOut.connect(self.send_log)
		self.send_barrage.is_finish.connect(self.check_finish)

	def show_my_self(self):
		self.show()

	def set_log_browser_style(self):
		self.log_browser.setGeometry(1, 300, 1200, 500)
		self.log_browser.setStyleSheet("""background:#E98316""")
		self.log_browser.setGraphicsEffect(QGraphicsOpacityEffect(self).setOpacity(0.5))

	def set_btn_get_room_data_style(self):
		self.btn_get_room_data.setGeometry(900, 25, 110, 30)
		self.btn_get_room_data.setFont(QFont("Timers", 16))
		self.btn_get_room_data.clicked.connect(self.on_click_btn_get_room_data)

	def set_btn_send_barrage(self):
		self.btn_send_barrage.setGeometry(1020, 25, 110, 30)
		self.btn_send_barrage.setFont(QFont("Timers", 16))
		self.btn_send_barrage.clicked.connect(self.on_click_btn_send_barrage)

	def set_btn_login_douyu_style(self):
		self.btn_login_douyu.setGeometry(900, 65, 110, 30)
		self.btn_login_douyu.setFont(QFont("Timers", 16))
		self.btn_login_douyu.clicked.connect(self.on_click_btn_login_douyu)

	def set_btn_has_login_douyu_style(self):
		self.btn_has_login_douyu.setGeometry(1020, 65, 110, 30)
		self.btn_has_login_douyu.setFont(QFont("Timers", 12))
		self.btn_has_login_douyu.clicked.connect(self.on_click_btn_has_login_douyu)

	def set_btn_login_huya_style(self):
		self.btn_login_huya.setGeometry(900, 105, 110, 30)
		self.btn_login_huya.setFont(QFont("Timers", 16))
		self.btn_login_huya.clicked.connect(self.on_click_btn_login_huya)

	def set_btn_has_login_huya_style(self):
		self.btn_has_login_huya.setGeometry(1020, 105, 110, 30)
		self.btn_has_login_huya.setFont(QFont("Timers", 12))
		self.btn_has_login_huya.clicked.connect(self.on_click_btn_has_login_huya)

	def on_click_btn_has_login_douyu(self):
		if url_pool.douyu_cookies == {}:
			self.log_browser.setText(get_log_str("没有登陆成功"))
			config.PlatFormLogin.DOU_YU = False
		else:
			self.log_browser.setText(get_log_str("登陆成功"))
			config.PlatFormLogin.DOU_YU = True

	def on_click_btn_has_login_huya(self):
		pass

	def on_click_btn_login_douyu(self):
		self.send_barrage.login()

	def on_click_btn_login_huya(self):
		pass

	def on_click_btn_get_room_data(self):
		self.btn_get_room_data.setEnabled(False)
		self.btn_send_barrage.setEnabled(False)
		self.worker.start()

	def on_click_btn_send_barrage(self):
		self.btn_get_room_data.setEnabled(False)
		self.btn_send_barrage.setEnabled(False)
		self.send_barrage.start()

	def check_finish(self, is_finish):
		if is_finish:
			self.btn_get_room_data.setEnabled(True)
			self.btn_send_barrage.setEnabled(True)

	def send_log(self, msg):
		self.log_browser.setText(msg)


# def start():
# 	# app = QApplication(sys.argv)
# 	view_main = ViewMain()
# 	view_main.show()
# # sys.exit(app.exec_())
