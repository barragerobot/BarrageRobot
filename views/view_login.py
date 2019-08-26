# -*- coding: utf-8 -*-
import os
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPalette, QColor, QFont
import re
import util

import config
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QRadioButton, QPushButton, QMainWindow


class ViewLogin(QMainWindow, QThread):
	is_finish_login = pyqtSignal(bool)

	def __init__(self):
		super().__init__()
		self.setWindowTitle(config.view_title)
		self.view_w = 600
		self.view_h = 400
		self.resize(self.view_w, self.view_h)
		self.setMaximumSize(self.view_w, self.view_h)
		self.setMinimumSize(self.view_w, self.view_h)

		palette1 = QPalette()
		palette1.setColor(self.backgroundRole(), QColor(113, 175, 164))
		self.setPalette(palette1)

		# setGeometry(9,9,50,25)
		# 从屏幕上(9,9)位置开始(即为最左上角的点),显示一个50*25的界面(宽50,高25)
		#
		# 账号输入框
		self.input_account = QLineEdit(self)
		self.input_account.setPlaceholderText("账号,6至15个字母或下划线组成")
		self.input_account.setGeometry(int(self.view_w / 4), int(self.view_h / 4), 290, 30)
		self.input_account.setFont(QFont("Timers", 16))
		self.input_account.setMaxLength(16)

		# 密码输入框
		self.input_password = QLineEdit(self)
		self.input_password.setEchoMode(QLineEdit.Password)
		self.input_password.setPlaceholderText("密码,6至15个字母或下划线组成")
		self.input_password.setGeometry(int(self.view_w / 4), int(self.view_h / 4) + 40, 290, 30)
		self.input_password.setFont(QFont("Timers", 16))
		self.input_password.setMaxLength(16)

		# 是否显示密码 check框
		self.btn_is_show_password = QRadioButton("显示密码", self)
		# self.btn_is_show_password.setStyleSheet('''color: rgb(0,0,0);;''')
		self.btn_is_show_password.setGeometry(int(self.view_w / 4), int(self.view_h / 4) + 40 + 40, 290, 30)
		self.btn_is_show_password.setFont(QFont("Timers", 16))
		self.btn_is_show_password.clicked.connect(self.show_password)

		# 登陆按钮
		self.btn_login = QPushButton("登录", self)
		self.btn_login.setGeometry(int(self.view_w / 4), int(self.view_h / 4) + 40 + 40 + 40, 100, 30)
		self.btn_login.setFont(QFont("Timers", 16))
		self.btn_login.clicked.connect(self.on_click_login_btn)

		# 注册按钮
		self.btn_register = QPushButton("注册", self)
		self.btn_register.setGeometry(int(self.view_w / 4) + 190, int(self.view_h / 4) + 40 + 40 + 40, 100, 30)
		self.btn_register.setFont(QFont("Timers", 16))
		self.btn_register.clicked.connect(self.on_click_register_btn)

	def show_password(self):
		if self.btn_is_show_password.isChecked():
			self.input_password.setEchoMode(QLineEdit.Normal)
		else:
			self.input_password.setEchoMode(QLineEdit.Password)

	def on_click_login_btn(self):
		input_account = self.input_account.text()
		input_password = self.input_password.text()

		try:
			if self.check_account(is_login=True, account=input_account, password=input_password):
				# util.write_json_file(config.account_path, data={"account": input_account, "password": input_password})

				self.is_finish_login.emit(True)
				self.hide()

			else:
				QMessageBox.warning(self, "!", "账号或密码错误", QMessageBox.Yes)
		except FileNotFoundError:
			QMessageBox.warning(self, "!", "账号或密码错误", QMessageBox.Yes)

	def on_click_register_btn(self):

		input_account = self.input_account.text()
		input_password = self.input_password.text()
		if os.path.exists(config.account_path):
			QMessageBox.warning(self, "!", "不要给老子重复注册！！", QMessageBox.Yes)
			return
		if self.check_account(is_login=False, account=input_account, password=input_password):
			register_time = int(time.time())
			user_data = {
				"account": input_account,
				"password": input_password,
				"start_time": register_time,
				"end_time": register_time + 24 * 3600}

			user_data = self.encrypt(str(user_data))
			util.write_data(config.account_path, data=user_data)
			# util.write_json_file(config.account_path, data=user_data)
			self.is_finish_login.emit(True)
			self.hide()
		else:
			QMessageBox.warning(self, "!", "账号或密码错误", QMessageBox.Yes)

	@staticmethod
	def encrypt(encrypt_str):
		target_str = ""
		for char_str in encrypt_str:
			target_str += chr(ord(char_str) + 4)
		return target_str

	@staticmethod
	def decode_str(encrypt_str):
		target_str = ""
		for char_str in encrypt_str:
			target_str += chr(ord(char_str) - 4)
		return target_str

	def check_account(self, is_login, account, password):
		print(account, password)
		if is_login:
			account_info = util.read_file(config.account_path)
			print("first", account_info)
			account_info = self.decode_str(account_info)
			print("second", account_info)
			print(type(account_info))
			account_info = eval(account_info)
			print("third", account_info)
			check_account = account_info["account"] == account
			check_password = account_info["password"] == password
		else:
			check_account = re.match(r"[0-9a-zA-Z\_]{6,16}", account) and len(account) <= 16
			check_password = re.match(r"[0-9a-zA-Z\_]{6,16}", password) and len(password) <= 16
			print("check account : %s" % check_account)
			print("check password : %s" % check_password)
		if check_account and check_password:
			return True
		else:
			return False

	# noinspection PyTypeChecker
	def closeEvent(self, event):
	
		reply = QMessageBox.question(self, 'Msg', "确定退出？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
	
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()
