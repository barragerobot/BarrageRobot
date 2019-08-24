# -*- coding: utf-8 -*-

import sys
import config
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QTextBrowser, QGraphicsOpacityEffect
from PyQt5.QtGui import QIcon, QFont, QPalette, QBrush, QPixmap


class ScreeSize(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height


class ViewMain(QMainWindow):
    def __init__(self, view_size: ScreeSize, scree_size: ScreeSize):
        super().__init__()
        self.is_init = True

        self.view_size = view_size
        self.scree_size = scree_size
        self.setWindowTitle(config.view_title)

        self.resize(self.view_size.width, self.view_size.height)
        self.setMaximumSize(self.view_size.width, self.view_size.height)
        self.setMinimumSize(self.view_size.width, self.view_size.height)
        self.move((int(self.scree_size.width - self.view_size.width) / 2), (
                int(self.scree_size.height - self.view_size.height) / 2))

        # self.scree_size = scree_size
        # self.setWindowTitle("弹幕自动化")
        # self.resize(1300, 800)
        # self.move(int((self.scree_size.width - 1200) / 2), int((self.scree_size.height - 800) / 2))
        self.setWindowIcon(QIcon(config.logo_path))
        window_platte = QPalette()  # 设置背景图片
        window_platte.setBrush(self.backgroundRole(), QBrush(QPixmap(config.background_path)))
        self.setPalette(window_platte)
        self.platform_input_box = QComboBox(self)
        self.fans_min_input_box = QComboBox(self)
        self.fans_max_input_box = QComboBox(self)
        self.cache_input_box = QComboBox(self)
        self.log_browser = QTextBrowser(self)
        self.platform_set()
        self.fans_min_set()
        self.fans_max_set()
        self.cache_use_set()
        self.log_browser_filed_set()
        self.show()

    def platform_set(self):
        platform = QLabel(self)  # QLabel实例化时，需传self（原因待了解）
        platform.setGeometry(20, 30, 110, 25)  # x=20px+80px=100px  y=  40px+40
        # platform.setStyleSheet("color:red")
        platform.setFont(QFont("Timers", 16))
        platform.setText("平台设置")
        self.platform_input_box.setGeometry(140, 25, 110, 30)  # 35-25=10/2=5 上下多5个像素
        self.platform_input_box.setFont(QFont("Timers", 14))
        self.platform_input_box.addItems(["所有", "斗鱼", "虎牙"])

    def fans_min_set(self):
        fans_min = QLabel(self)
        fans_min.setGeometry(280, 30, 110, 25)
        fans_min.setFont(QFont("Timer", 16))
        fans_min.setText("粉丝下限")
        self.fans_min_input_box.setGeometry(400, 25, 110, 30)
        self.fans_min_input_box.setFont(QFont("Timers", 14))
        self.fans_min_input_box.addItems(["0", "100", "300"])

    def fans_max_set(self):
        fans_max = QLabel(self)
        fans_max.setGeometry(530, 30, 110, 25)
        fans_max.setFont(QFont("Timers", 16))
        fans_max.setText("粉丝上限")
        self.fans_max_input_box.setGeometry(650, 25, 110, 30)
        self.fans_max_input_box.setFont(QFont("Timers", 14))
        self.fans_max_input_box.addItems(["500000", "100000", "200000", "300000"])

    def cache_use_set(self):
        cache = QLabel(self)
        cache.setGeometry(780, 30, 110, 25)
        cache.setFont(QFont("Timers", 16))
        cache.setText("使用缓存")
        self.cache_input_box.setGeometry(900, 25, 110, 30)
        self.cache_input_box.setFont(QFont("Timers", 14))
        self.cache_input_box.addItems(["是", "否"])

    def log_browser_filed_set(self):
        log_browser_filed_name = QLabel(self)
        log_browser_filed_name.setGeometry(20, 250, 160, 40)
        log_browser_filed_name.setFont(QFont("Timers", 14))
        log_browser_filed_name.setText("弹幕日志")
        self.log_browser.setGeometry(20, 300, 1260, 480)
        self.log_browser.setStyleSheet("""background:#E98316""")  # “#167ce9”
        op = QGraphicsOpacityEffect(self)
        op.setOpacity(0.5)
        self.log_browser.setGraphicsEffect(op)

    def __init_timer(self):
        pass

    def on_click_test_button(self):
        self.close()


def view_start():
    app = QApplication(sys.argv)
    screen_rect = app.desktop().screenGeometry()
    scree = ScreeSize(height=screen_rect.height(), width=screen_rect.width())
    view_main_scree = ScreeSize(height=int(scree.height / 1.25), width=int(scree.width / 1.25))
    view_main = ViewMain(view_size=view_main_scree, scree_size=scree)
    view_main.show()

    sys.exit(app.exec_())
