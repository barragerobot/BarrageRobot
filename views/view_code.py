import os
import sys

from PyQt5.QtCore import QThread, pyqtSignal

import config
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication


class ViewShowQrCode(QWidget, QThread):
	# 日志信号
	log_msg = pyqtSignal(str)
	# 是否已扫码登陆信号
	is_login = pyqtSignal(bool)

	def __init__(self, code_path, view_size: tuple):
		super().__init__()
		self.setWindowTitle(config.view_title)
		self.resize(view_size[0], view_size[1])
		self.setMaximumSize(view_size[0], view_size[1])
		self.setMinimumSize(view_size[0], view_size[1])
		window_pale = QtGui.QPalette()
		window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(code_path)))
		self.setPalette(window_pale)

	# noinspection PyTypeChecker
	def closeEvent(self, event):

		reply = QMessageBox.question(self, 'Msg', "已登陆?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

		if reply == QMessageBox.Yes:
			self.is_login.emit(True)
			event.accept()
		else:
			event.ignore()


def qr_code(path, w, h):
	app = QApplication(sys.argv)
	a = ViewShowQrCode(path, (w, h))
	a.show()
	sys.exit(app.exec_())
