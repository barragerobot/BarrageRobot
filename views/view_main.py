# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QTextBrowser, QGraphicsOpacityEffect
from PyQt5.QtWidgets import QPushButton
from logic import url_pool
import sys
import config
import time
import requests
import bs4
import traceback


def get_log_str(msg: str):
	now_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	if len(config.log_text_str) > 5000:
		config.log_text_str = ""
	if config.log_text_str == "":
		config.log_text_str = now_time + " -> " + msg
	else:
		config.log_text_str = now_time + " -> " + msg + "\n" + config.log_text_str

	return config.log_text_str


class RoomStatistics(QThread):
	sinOut = pyqtSignal(str)

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

		self.worker = RoomStatistics()
		self.worker.sinOut.connect(self.send_log)

	def set_log_browser_style(self):
		self.log_browser.setGeometry(1, 300, 1200, 500)
		self.log_browser.setStyleSheet("""background:#E98316""")
		self.log_browser.setGraphicsEffect(QGraphicsOpacityEffect(self).setOpacity(0.5))

	def set_btn_get_room_data_style(self):
		self.btn_get_room_data.setGeometry(900, 25, 110, 30)
		self.btn_get_room_data.setFont(QFont("Timers", 16))
		self.btn_get_room_data.clicked.connect(self.on_click_btn_get_room_data)

	def set_btn_send_barrage(self):
		self.btn_send_barrage.setGeometry(900, 25, 110, 30)

	def on_click_btn_get_room_data(self):
		self.btn_get_room_data.setEnabled(False)
		self.worker.start()

	def send_log(self, msg):
		self.log_browser.setText(msg)
		if not self.worker.working:
			self.btn_get_room_data.setEnabled(True)


def start():
	app = QApplication(sys.argv)
	view_main = ViewMain()
	view_main.show()
	sys.exit(app.exec_())
