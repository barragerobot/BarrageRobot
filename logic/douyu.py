# -*- coding: utf-8 -*-
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import json
import bs4
import time
import config
import requests
import logging


class UrlGenerator(object):

	def __init__(self):
		self.douyu_base_url = "https://www.douyu.com"

		self.browser = None

		self.douyu_cookies = dict()
		self.directory_games = dict()

		self.douyu_game_type = list()

		# 有效斗鱼房间列表 - 不包含已经拥有工会或者官方直播间
		self.douyu_rooms = list()

		# 有效虎牙房间列表 - 不包含已经拥有工会或者官方直播间
		self.huya_rooms = list()

	def init_browser(self):
		chrome_options = Options()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		self.browser = webdriver.Chrome(chrome_options=chrome_options)

	def get_douyu_directory(self):
		self.browser.get(self.douyu_base_url + "/directory")
		soup_menu = bs4.BeautifulSoup(self.browser.page_source, "html.parser")
		for data in soup_menu.select("script"):
			data = str(data)
			if "DATA" in data:
				data = data.split("var $DATA =")[-1].split(";")[0]
				return json.loads(data)

	def get_douyu_type_platform(self):
		# 获取斗鱼平台直播的所有房间
		self.browser.get(self.douyu_base_url + "/directory")

		soup_menu = bs4.BeautifulSoup(self.browser.page_source, "html.parser")

		for data in soup_menu.select("script"):
			data = str(data)
			if "DATA" in data:
				data = data.split("var $DATA =")[-1].split(";")[0]
				self.directory_games = json.loads(data)
				print(self.directory_games)

		# 所有游戏类型,包含游戏名称列表
		category_list = self.directory_games["firstCategory"]

		# 游戏名称 eg.LOL
		game_relative_path_list = []

		for category in category_list:
			for relative in category["secondCategory"]:
				game_relative_path_list.append(relative["cate2Url"])

		for game_relative_path in game_relative_path_list:
			url = self.douyu_base_url + game_relative_path
			self.douyu_game_type.append(url)

		return self.douyu_game_type


#
# def get_douyu_rooms(self):
# 	# TODO 获取房间属性 -- 关注量，名称等等，用于实现筛选功能，过滤官方直播间。可用class 描述属性实现
# 	for game_url in self.douyu_game_type:
# 		time.sleep(config.request_wait_time)
# 		game_url_result = requests.get(game_url)
# 		if game_url_result.status_code == 200:
# 			logging.info("%s 访问成功" % game_url)
# 		else:
# 			logging.error("%s 访问失败" % game_url)
# 			continue
# 		soup_game = bs4.BeautifulSoup(game_url_result.text, "html.parser")
#
# 		game_room_list = soup_game.select(".layout-Cover-item")
#
# 		for game_room in game_room_list:
# 			self.douyu_rooms.append("%s/%s" % (self.douyu_base_url, game_room.select("a")[0].get("href")))
#
# 	logging.info("斗鱼旗下所有直播间的数量为 : %s" % len(self.douyu_rooms))
# 	return self.douyu_rooms


url_pool = UrlGenerator()
