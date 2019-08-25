from PIL import Image

import config
import time
import os
from views import qr_code

xpath_login_top = '//*[@id="js-header"]/div/div/div[3]/div[7]/div/div'
# //*[@id="js-header"]/div/div/div[3]/div[7]/div/div/a/span

xpath_input = '//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/textarea'
xpath_send = '//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/div[2]'
url = "https://passport.douyu.com/index/login?passport_reg_callback=PASSPORT_REG_SUCCESS_CALLBACK&passport_login_callback=PASSPORT_LOGIN_SUCCESS_CALLBACK&passport_close_callback=PASSPORT_CLOSE_CALLBACK&passport_dp_callback=PASSPORT_DP_CALLBACK&type=login&client_id=1&state=https%3A%2F%2Fwww.douyu.com%2F"
xpath_qr_code = '//*[@id="login-passport-frame"]'
config.chrome_browser.get(url)
# time.sleep(config.wait_time_max)
config.chrome_browser.maximize_window()
# config.chrome_browser.set_page_load_timeout(config.wait_time_max)

# config.chrome_browser.find_element_by_xpath(xpath_news).click()

config.chrome_browser.set_page_load_timeout(config.wait_time_max)
time.sleep(config.wait_time_max)
# config.write_data("E:\\work_bill\\BarrageRobot\\resource\\22.html", config.chrome_browser.page_source)
# self.chrome_browser.save_screenshot("E:\\work_bill\\BarrageRobot\\resource\\image\\scree.png")

# img_element = config.chrome_browser.find_element_by_xpath(xpath_qr_code)
# locations = img_element.location
# print("locations : %s" % locations)
# sizes = img_element.size
# print("sizes : %s" % sizes)
# rangle = (int(locations['x']), int(locations['y']), int(locations['x'] + sizes['width']),
# 		  int(locations['y'] + sizes['height']))
# path_1 = os.getcwd() + "\\resource\\image\\code_1.png"
# path_2 = os.getcwd() + "\\resource\\image\\code_2.png"
# config.chrome_browser.save_screenshot(path_1)
# img = Image.open(str(path_1))
#
# jpg = img.crop(rangle)
#
# jpg.save(str(path_2))
# qr_code(path=path_2, w=400, h=515)
config.chrome_browser.get("https://www.douyu.com/6969129")
time.sleep(config.wait_time_max)
input_box = config.chrome_browser.find_element_by_xpath(xpath_input)
input_box.click()
time.sleep(1)
input_box.send_keys("li hai li hai")
send_btn = config.chrome_browser.find_element_by_xpath(xpath_send)
send_btn.click()