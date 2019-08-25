# -*- coding: utf-8 -*-
# from views import view_start, start, qr_code
from PyQt5.QtWidgets import QApplication

from views import ViewLogin, ViewMain
import sys

# import threading

if __name__ == "__main__":
	# import win32api
	# import win32con
	#
	app = QApplication(sys.argv)
	view_login = ViewLogin()
	view_main = ViewMain()
	view_login.show()
	view_login.is_finish_login.connect(view_main.show)
	sys.exit(app.exec_())
