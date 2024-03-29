# -*- coding: utf-8 -*-
import os
import configparser

from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def get_ini_data(ini_path: str, section: str, section_item: str) -> str:
	conf = configparser.ConfigParser()
	conf.read(filenames=ini_path, encoding="UTF-8")
	section_name = section
	section = conf.items(section=section_name)
	conf_section_data = {}
	for (key, value) in section:
		conf_section_data.setdefault(key, value)
	try:
		if section_name == "path":
			if section_item in conf_section_data.keys():
				section_data = "%s%s" % (os.getcwd(), conf_section_data[section_item])
			else:
				section_data = str()
			return section_data
		else:
			return conf_section_data[section_item]
	except KeyError:
		raise KeyError("Not Find '%s' In %s" % (section_item, section))


def write_data(write_path: str, data: str, mode="w", encoding="UTF-8"):
	with open(write_path, mode, encoding=encoding) as wr:
		wr.write(data)


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# chrome_options=chrome_options
# executable_path=os.getcwd() + "\\chromedriver", chrome_options=chrome_options
# webdriver.Chrome()
chrome_browser = None

conf_path = os.path.join(os.getcwd(), "resource/conf.ini")
logo_path = get_ini_data(ini_path=conf_path, section="path", section_item="logo_path")
our_path = get_ini_data(ini_path=conf_path, section="path", section_item="our_path")
background_path = get_ini_data(ini_path=conf_path, section="path", section_item="background_path")
account_path = get_ini_data(ini_path=conf_path, section="path", section_item="account_path")
cookies_path = get_ini_data(ini_path=conf_path, section="path", section_item="cookies_path")


log_text_str = ""

view_title = "弹幕机器人 ---------- Bill Is Most Handsome Of The World ---------- "
parting_line = "-" * 200
# #### 默认请求间隔时间
request_wait_time = 1
# #### 两次弹幕发送间隔时间
send_text_wait_time = 60
# #### 加载网页最长等待时间
wait_time_max = 30


class PlatFormLogin(object):
	DOU_YU = False
	HU_YA = False


class Platform(object):
	ALL = 0
	DOU_YU = 1
	HU_YA = 2


class Params(object):
	# #### 初始全平台
	plat_form = Platform.ALL
	fans_max = 9999999999
	fans_min = 0
	is_use_cache = True
