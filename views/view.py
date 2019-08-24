# -*- coding: utf-8 -*-

import json
import sys
import time

import bs4
import itchat
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QTextBrowser, QGraphicsOpacityEffect
from PyQt5.QtWidgets import QPushButton
from selenium import webdriver

import config
from logic import url_pool


def send_log_text(msg: str):
	now_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	if config.log_text_str == "":
		config.log_text_str = now_time + " -> " + msg
	else:
		config.log_text_str = now_time + " -> " + msg + "\n" + config.log_text_str

	return config.log_text_str


class ScreeSize(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height


class WorkerThread(QThread):
	trigger = pyqtSignal()

	def __init__(self):
		super(WorkerThread, self).__init__()
		self.browser = None
		self.directory_games = None
		self.douyu_base_url = "https://www.douyu.com"

	def get_douyu_rooms(self, send_msg):
		send_log_text("正在扫描斗鱼旗下所有分类列表,稍候........").connect(send_msg)
		self.log_browser.setText(send_log_text())
		self.browser = webdriver.PhantomJS()
		# 获取斗鱼平台直播的所有房间
		self.browser.get(self.douyu_base_url + "/directory")
		soup_menu = bs4.BeautifulSoup(self.browser.page_source, "html.parser")
		for data in soup_menu.select("script"):
			data = str(data)
			if "DATA" in data:
				data = data.split("var $DATA =")[-1].split(";")[0]
				self.directory_games = json.loads(data)

		# 所有游戏类型,包含游戏名称列表
		category_list = self.directory_games["firstCategory"]

		# 游戏名称 eg.LOL
		game_relative_path_list = []
		game_url_list = []

		for category in category_list:
			for relative in category["secondCategory"]:
				game_relative_path_list.append(relative["cate2Url"])

		for game_relative_path in game_relative_path_list:
			url = self.douyu_base_url + game_relative_path
			game_url_list.append(url)
		send_log_text("斗鱼旗下所有分类列表扫描完毕,共 %s 个分类" % len(game_url_list)).connect(send_msg)
		self.trigger.emit()
	# self.log_browser.setText(send_log_text("斗鱼旗下所有分类列表扫描完毕,共 %s 个分类" % len(game_url_list)))

	# self.log_browser.setText(send_log_text("正在扫描斗鱼旗下所有房间,此过程可能需要花费一些时间，稍候........"))
	# for game_url in game_url_list:
	# 	time.sleep(config.request_wait_time)
	# 	game_url_result = requests.get(game_url)
	# 	if game_url_result.status_code == 200:
	# 		send_log_text("%s 访问成功" % game_url)
	# 	else:
	# 		send_log_text("%s 访问失败" % game_url)
	# 		continue
	# 	soup_game = bs4.BeautifulSoup(game_url_result.text, "html.parser")
	#
	# 	game_room_list = soup_game.select(".layout-Cover-item")
	#
	# 	for game_room in game_room_list:
	# 		self.douyu_rooms.append("%s/%s" % (self.douyu_base_url, game_room.select("a")[0].get("href")))
	# self.log_browser.setText(send_log_text("斗鱼旗下所有房间扫描完毕，一共 %s 个房间" % len(self.douyu_rooms)))


class ViewMain(QMainWindow):
	def __init__(self, view_size: ScreeSize, scree_size: ScreeSize):
		super().__init__()
		self.douyu_base_url = "https://www.douyu.com"
		self.browser = None
		self.directory_games = dict()
		self.douyu_rooms = list()

		self.is_init = True
		self.we_chat_is_login = False
		self.log_text_str = ""

		self.view_size = view_size
		self.scree_size = scree_size
		self.setWindowTitle(config.view_title)

		self.resize(self.view_size.width, self.view_size.height)
		self.setMaximumSize(self.view_size.width, self.view_size.height)
		self.setMinimumSize(self.view_size.width, self.view_size.height)
		self.move((int(self.scree_size.width - self.view_size.width) / 2), (
				int(self.scree_size.height - self.view_size.height) / 2))
		self.setWindowIcon(QIcon(config.logo_path))

		palette1 = QPalette()
		palette1.setColor(self.backgroundRole(), QColor(113, 175, 164))
		self.setPalette(palette1)

		self.platform_input_box = QComboBox(self)
		self.fans_min_input_box = QComboBox(self)
		self.fans_max_input_box = QComboBox(self)
		self.cache_input_box = QComboBox(self)
		self.log_browser = QTextBrowser(self)
		self.btn_login_we_chat = QPushButton("登陆微信", self)
		self.btn_get_room_data = QPushButton("扫描房间", self)
		self.worker = WorkerThread()
		self.platform_set()
		self.fans_min_set()
		self.fans_max_set()
		self.cache_use_set()
		self.log_browser_filed_set()
		self.we_chat_login_set()
		self.btn_get_room_data_set()

	def set_log_browser_text(self, msg):
		self.log_browser.setText(msg)

	def platform_set(self):
		platform = QLabel(self)  # QLabel实例化时，需传self（原因待了解）
		platform.setGeometry(20, 30, 110, 25)  # x=20px+80px=100px  y=  40px+40
		# platform.setStyleSheet("color:red")
		platform.setFont(QFont("Timers", 16))
		platform.setText("平台设置")
		self.platform_input_box.setGeometry(140, 25, 110, 30)  # 35-25=10/2=5 上下多5个像素
		self.platform_input_box.setFont(QFont("Timers", 14))
		self.platform_input_box.addItems(["所有", "斗鱼", "虎牙"])
		self.platform_input_box.activated[str].connect(self.choose_platform)

	def fans_min_set(self):
		fans_min = QLabel(self)
		fans_min.setGeometry(280, 30, 110, 25)
		fans_min.setFont(QFont("Timer", 16))
		fans_min.setText("粉丝下限")
		self.fans_min_input_box.setGeometry(400, 25, 110, 30)
		self.fans_min_input_box.setFont(QFont("Timers", 14))
		self.fans_min_input_box.addItems(["不限", "5000", "10000", "50000"])
		self.fans_min_input_box.activated[str].connect(self.choose_min_fans)

	def fans_max_set(self):
		fans_max = QLabel(self)
		fans_max.setGeometry(530, 30, 110, 25)
		fans_max.setFont(QFont("Timers", 16))
		fans_max.setText("粉丝上限")
		self.fans_max_input_box.setGeometry(650, 25, 110, 30)
		self.fans_max_input_box.setFont(QFont("Timers", 14))
		self.fans_max_input_box.addItems(["不限", "50万", "100万", "200万"])
		self.fans_max_input_box.activated[str].connect(self.choose_max_fans)

	def cache_use_set(self):
		cache = QLabel(self)
		cache.setGeometry(780, 30, 110, 25)
		cache.setFont(QFont("Timers", 16))
		cache.setText("使用缓存")
		self.cache_input_box.setGeometry(900, 25, 110, 30)
		self.cache_input_box.setFont(QFont("Timers", 14))
		self.cache_input_box.addItems(["是", "否"])
		self.cache_input_box.activated[str].connect(self.choose_cache)

	def we_chat_login_set(self):
		self.btn_login_we_chat.setGeometry(1050, 25, 110, 30)
		self.btn_login_we_chat.setFont(QFont("Timers", 16))
		self.btn_login_we_chat.clicked.connect(self.on_click_btn_we_chat)

	def btn_get_room_data_set(self):
		self.btn_get_room_data.setGeometry(1200, 25, 110, 30)
		self.btn_get_room_data.setFont(QFont("Timers", 16))
		self.btn_get_room_data.clicked.connect(self.on_click_btn_room_data)

	def log_browser_filed_set(self):
		# log_browser_filed_name = QLabel(self)
		# log_browser_filed_name.setGeometry(20, 250, 160, 40)
		# log_browser_filed_name.setFont(QFont("Timers", 14))
		# log_browser_filed_name.setText("弹幕日志")
		QApplication.processEvents()
		self.log_browser.setGeometry(1, 300, 1525, 500)
		self.log_browser.setStyleSheet("""background:#E98316""")  # “#167ce9”
		op = QGraphicsOpacityEffect(self)
		op.setOpacity(0.5)
		self.log_browser.setGraphicsEffect(op)

	def on_click_btn_we_chat(self):
		self.log_browser.setText(send_log_text("若没有提示登陆成功，扫码登陆微信或者手机同意登陆"))
		if not self.we_chat_is_login:
			itchat.auto_login(hotReload=True)
			self.we_chat_is_login = True
			self.log_browser.setText(send_log_text("微信登陆成功"))
		else:
			self.log_browser.setText(send_log_text("微信已经登陆了，不要重复点"))

	def choose_min_fans(self, choose_fans_min_text):
		choose_fans_min_text = str(choose_fans_min_text)
		if choose_fans_min_text == "5000":
			config.Params.fans_min = 5000
			self.log_browser.setText(send_log_text("粉丝下限设置为5000"))
		elif choose_fans_min_text == "10000":
			config.Params.fans_min = 10000
			self.log_browser.setText(send_log_text("粉丝下限设置为10000"))
		elif choose_fans_min_text == "50000":
			config.Params.fans_min = 50000
			self.log_browser.setText(send_log_text("粉丝下限设置为50000"))
		else:
			config.Params.fans_min = 0
			self.log_browser.setText(send_log_text("不限粉丝下限"))

	def choose_max_fans(self, choose_fans_max_text):
		choose_fans_max_text = str(choose_fans_max_text)
		if choose_fans_max_text == "50万":
			config.Params.fans_max = 500000
			self.log_browser.setText(send_log_text("粉丝上限设置为50万"))
		elif choose_fans_max_text == "100万":
			config.Params.fans_max = 1000000
			self.log_browser.setText(send_log_text("粉丝下限设置为100万"))
		elif choose_fans_max_text == "200万":
			config.Params.fans_max = 2000000
			self.log_browser.setText(send_log_text("粉丝下限设置为200万"))
		else:
			config.Params.fans_min = 9999999999
			self.log_browser.setText(send_log_text("不限粉丝下限"))

	def choose_platform(self, choose_fans_text):
		if choose_fans_text == "斗鱼":
			config.Params.plat_form = config.Platform.DOU_YU
			self.log_browser.setText(send_log_text("选择了斗鱼平台，platform : %s" % config.Params.plat_form))
		elif choose_fans_text == "虎牙":
			config.Params.plat_form = config.Platform.HU_YA
			self.log_browser.setText(send_log_text("选择了虎牙平台，platform : %s" % config.Params.plat_form))
		else:
			config.Params.plat_form = config.Platform.ALL
			self.log_browser.setText(send_log_text("不限平台，platform : %s" % config.Params.plat_form))

	def choose_cache(self, choose_cache_text):
		if choose_cache_text == "是":
			config.Params.is_use_cache = True
			self.log_browser.setText(send_log_text("当前选择使用缓存"))
		elif choose_cache_text == "否":
			config.Params.is_use_cache = False
			self.log_browser.setText(send_log_text("当前选择不使用缓存"))

	def get_douyu_rooms(self):
		self.log_browser.setText(send_log_text("正在扫描斗鱼旗下所有分类列表,稍候........"))
		self.browser = webdriver.PhantomJS()
		# 获取斗鱼平台直播的所有房间
		self.browser.get(self.douyu_base_url + "/directory")
		soup_menu = bs4.BeautifulSoup(self.browser.page_source, "html.parser")
		for data in soup_menu.select("script"):
			data = str(data)
			if "DATA" in data:
				data = data.split("var $DATA =")[-1].split(";")[0]
				self.directory_games = json.loads(data)

		# 所有游戏类型,包含游戏名称列表
		category_list = self.directory_games["firstCategory"]

		# 游戏名称 eg.LOL
		game_relative_path_list = []
		game_url_list = []

		for category in category_list:
			for relative in category["secondCategory"]:
				game_relative_path_list.append(relative["cate2Url"])

		for game_relative_path in game_relative_path_list:
			url = self.douyu_base_url + game_relative_path
			game_url_list.append(url)

		self.log_browser.setText(send_log_text("斗鱼旗下所有分类列表扫描完毕,共 %s 个分类" % len(game_url_list)))

		self.log_browser.setText(send_log_text("正在扫描斗鱼旗下所有房间,此过程可能需要花费一些时间，稍候........"))
		for game_url in game_url_list:
			time.sleep(config.request_wait_time)
			game_url_result = requests.get(game_url)
			if game_url_result.status_code == 200:
				send_log_text("%s 访问成功" % game_url)
			else:
				send_log_text("%s 访问失败" % game_url)
				continue
			soup_game = bs4.BeautifulSoup(game_url_result.text, "html.parser")

			game_room_list = soup_game.select(".layout-Cover-item")

			for game_room in game_room_list:
				self.douyu_rooms.append("%s/%s" % (self.douyu_base_url, game_room.select("a")[0].get("href")))
		self.log_browser.setText(send_log_text("斗鱼旗下所有房间扫描完毕，一共 %s 个房间" % len(self.douyu_rooms)))
		return self.douyu_rooms

	def on_click_btn_room_data(self):
		if config.Params.plat_form == config.Platform.DOU_YU:
			self.worker.get_douyu_rooms(self.log_browser.setText)
			# self.log_browser.setText(send_log_text("开始扫描斗鱼旗下所有分类列表,稍候........"))
			# self.log_browser.update()
			# self.log_browser.setText(send_log_text("初始化"))
			# self.log_browser.update()
			url_pool.init_browser()
			# self.log_browser.setText(send_log_text("初始化完毕"))
			# self.log_browser.update()
		# chrome_options = Options()
		# chrome_options.add_argument('--headless')
		# chrome_options.add_argument('--disable-gpu')
		# self.browser = webdriver.Chrome(chrome_options=chrome_options)
		# self.log_browser.setText(send_log_text("初始化chrome"))
		# # 获取斗鱼平台直播的所有房间
		# self.browser.get(self.douyu_base_url + "/directory")
		# import pprint
		# pprint.pprint(self.browser.page_source)
		# soup_menu = bs4.BeautifulSoup(self.browser.page_source, "html.parser")
		# for data in soup_menu.select("script"):
		# 	data = str(data)
		# 	if "DATA" in data:
		# 		data = data.split("var $DATA =")[-1].split(";")[0]
		# 		self.directory_games = json.loads(data)
		# # 所有游戏类型,包含游戏名称列表
		# category_list = self.directory_games["firstCategory"]
		#
		# # 游戏名称 eg.LOL
		# game_relative_path_list = []
		# game_url_list = []
		#
		# for category in category_list:
		# 	for relative in category["secondCategory"]:
		# 		game_relative_path_list.append(relative["cate2Url"])
		#
		# for game_relative_path in game_relative_path_list:
		# 	url = self.douyu_base_url + game_relative_path
		# 	game_url_list.append(url)
		#
		# self.log_browser.setText(self.log_text("斗鱼旗下所有分类列表扫描完毕,共 %s 个分类" % len(game_url_list)))
		#
		# self.log_browser.setText(self.log_text("正在扫描斗鱼旗下所有房间,此过程可能需要花费一些时间，稍候........"))
		# for game_url in game_url_list:
		# 	time.sleep(config.request_wait_time)
		# 	game_url_result = requests.get(game_url)
		# 	if game_url_result.status_code == 200:
		# 		self.log_text("%s 访问成功" % game_url)
		# 	else:
		# 		self.log_text("%s 访问失败" % game_url)
		# 		continue
		# 	soup_game = bs4.BeautifulSoup(game_url_result.text, "html.parser")
		#
		# 	game_room_list = soup_game.select(".layout-Cover-item")
		#
		# 	for game_room in game_room_list:
		# 		self.douyu_rooms.append("%s/%s" % (self.douyu_base_url, game_room.select("a")[0].get("href")))
		# self.log_browser.setText(self.log_text("斗鱼旗下所有房间扫描完毕，一共 %s 个房间" % len(self.douyu_rooms)))

		elif config.Params.plat_form == config.Platform.HU_YA:
			pass
		else:
			pass


def view_start():
	app = QApplication(sys.argv)
	screen_rect = app.desktop().screenGeometry()
	scree = ScreeSize(height=screen_rect.height(), width=screen_rect.width())
	view_main_scree = ScreeSize(height=int(scree.height / 1.25), width=int(scree.width / 1.25))
	view_main = ViewMain(view_size=view_main_scree, scree_size=scree)
	view_main.show()

	sys.exit(app.exec_())
