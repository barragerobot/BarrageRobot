#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import logging
import configparser
import pyautogui
import time
import threading

from logging.handlers import RotatingFileHandler

log_style = "%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d] : %(message)s"
logging.basicConfig(format=log_style, level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)


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
			
			if section_data == "":
				return section_data
			#
			# if not os.path.exists(section_data):
			# 	os.makedirs(section_data)
			# logging.debug("section_data : %s" % section_data)
			return section_data
		else:
			return conf_section_data[section_item]
	except KeyError:
		raise KeyError("Not Find '%s' In %s" % (section_item, section))


def read_json_file(file_path: str, mode="r", encoding="UTF-8") -> json:
	if not os.path.exists(path=file_path) or not os.path.isfile(path=file_path):
		raise FileNotFoundError("File Not Found,File Path : %s " % file_path)
	with open(file=file_path, mode=mode, encoding=encoding) as rd:
		return json.loads(rd.read())


def read_file(file_path: str, mode="r", encoding="UTF-8") -> json:
	if not os.path.exists(path=file_path) or not os.path.isfile(path=file_path):
		raise FileNotFoundError("File Not Found,File Path : %s " % file_path)
	with open(file=file_path, mode=mode, encoding=encoding) as fd:
		return fd.read()


def write_json_file(file_path: str, data: json, mode="w", encoding="UTF-8"):
	# if not os.path.exists(path=file_path) or not os.path.isfile(path=file_path):
	# 	raise FileNotFoundError("File Path Error,Need A File Not Dir")
	with open(file=file_path, mode=mode, encoding=encoding) as wd:
		json.dump(data, wd)


def write_data(write_path: str, data: str, mode="w", encoding="UTF-8"):
	with open(write_path, mode, encoding=encoding) as wr:
		wr.write(data)


def logger(log_name: str, log_path: str, log_lv=logging.DEBUG, mode="a+"):
	if not os.path.exists(log_path):
		os.makedirs(log_path)
	handler = RotatingFileHandler(os.path.join(log_path, log_name + ".log"), mode=mode)
	logging.getLogger("requests").setLevel(logging.WARNING)
	fmt = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
	fmt.datefmt = '%Y-%m-%d %H:%M:%S'
	handler.setFormatter(fmt)
	handler.setLevel(log_lv)
	
	kit_logger = logging.getLogger(log_name)
	kit_logger.addHandler(handler)
	kit_logger.root.setLevel(log_lv)
	
	return kit_logger


def list_to_str(data_list: list, separator: str = ":"):
	value_str = ""
	for data_idx in range(0, len(data_list)):
		if data_idx != len(data_list) - 1:
			value_str += "%s%s" % (data_list[data_idx], separator)
		else:
			value_str += "%s" % data_list[data_idx]
	logging.debug("str : %s" % value_str)
	return value_str


def dict_to_str(dict_data: dict, target_list: list, separator: str = ":"):
	for key, value in dict_data.items():
		try:
			target_list[key] = value
		except IndexError:
			logging.error("IndexError -> key : %s ,value : %s , list : %s " % (key, value, target_list))
			continue
	
	return list_to_str(target_list, separator)


class Position(object):
	x = -1
	y = -1


def position_click(click_interval_time=0.1, stay_time=3):
	stay_count = 0
	
	while True:
		position = pyautogui.position()
		# logging.info("stay_count : %s." % stay_count)
		# logging.info("position : (%s,%s)." % (position.x, position.y))
		if position.x == Position.x and position.y == Position.y:
			stay_count += 1
			if stay_count >= int(stay_time / click_interval_time):
				pyautogui.click(x=Position.x, y=Position.y)
				time.sleep(click_interval_time)
				continue
			time.sleep(click_interval_time)
			continue
		
		Position.x = position.x
		Position.y = position.y
		stay_count = 0
		time.sleep(click_interval_time)
		if Position.x == 0 and Position.y == 0:
			logging.info("position click ended")
			break
	return


def check_position():
	while True:
		position = pyautogui.position()
		thread_position_click = threading.Thread(target=position_click, name="click", args=(0.5,))
		if position[0] == 3839 and position[1] == 1079:
			thread_position_click.start()
			logging.info("position click start")
			thread_position_click.join()
			time.sleep(5)


def find_key_data(data, target_key):
	if isinstance(data, dict):
		if target_key in data.keys():
			return True
		for key, value in data.items():
			if isinstance(value, dict) or isinstance(value, list):
				if find_key_data(data=value, target_key=target_key):
					return True
				else:
					continue
			else:
				if value == target_key:
					return True
				else:
					continue
	elif isinstance(data, list):
		for value in data:
			if isinstance(value, dict) or isinstance(value, list):
				if find_key_data(data=value, target_key=target_key):
					return True
				else:
					continue
			else:
				if value == target_key:
					return True
				else:
					continue


def compare_value(object_a, object_b):
	if type(object_a) != type(object_b):
		logging.info("The data types are different")
		return False
	
	if id(object_a) == id(object_b):
		logging.info("They have the same memory address")
		return True
	
	if isinstance(object_a, list):
		object_a_length = len(object_a)
		object_b_length = len(object_b)
		
		if object_a_length != object_b_length:
			logging.info("They're list, but they're different lengths")
			return False
		for idx in range(0, object_a_length):
			if not compare_value(object_a[idx], object_b[idx]):
				logging.info(
					"Index of %s has a different value.A : %s , B : %s" % (idx, object_a[idx], object_b[idx]))
				return False
		return True
	elif isinstance(object_a, dict):
		object_a_length = len(object_a)
		object_b_length = len(object_b)
		
		if object_a_length != object_b_length:
			logging.info("They're dict, but they're different lengths")
			return False
		
		for key, value in object_a.items():
			if key not in object_b.keys():
				logging.info("%s in %s,but not in %s" % (key, object_a, object_b))
				return False
			
			if not compare_value(value, object_b[key]):
				logging.info("%s and %s have a different value" % (value, object_b[key]))
				return False
		return True
	elif isinstance(object_a, int) or isinstance(object_a, str) or isinstance(object_a, bool):
		if object_a == object_b:
			return True
		else:
			return False
	else:
		logging.error("Not Support")
		return False


def start_timer(t):
	start_time = time.time()
	
	while time.time() - start_time < t:
		print(int(time.time() - start_time))
		time.sleep(1)
