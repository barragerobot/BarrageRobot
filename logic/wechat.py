# -*- coding: utf-8 -*-

import itchat


class WeChat(object):
	def __init__(self):
		self.is_login = False

	def we_chat_login(self):
		itchat.auto_login(hotReload=True)
		self.is_login = True

	def send_msg(self, msg):
		itchat.send(msg, toUserName="filehelper")

	def send_image(self, image):
		itchat.send_image(image, toUserName="filehelper")


we_chat = WeChat
