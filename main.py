import selenium 
import seleniumrequests
from seleniumrequests import Chrome
import time
import os
from bs4 import BeautifulSoup
import pickle
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from PageParse import full_page_information
import pdb

NOW_PATH = os.getcwd()

# 开始前，先把chromedriver.exe放到当前文件夹下

# 完成登录
driver = Chrome()

driver.maximize_window()

driver.request("POST", "https://www.jianyu360.com/phone/login", 
            data={"reqType" : "phoneLogin","phone" : "13166301938","password" : "123456"})
driver.get("https://www.jianyu360.com/jylab/supsearch/index.html")

keywords = "智能 图像"
month = "6月"

#输入关键词
searchInput = driver.find_element_by_id("searchinput")
searchInput.send_keys(keywords)
searchInput.send_keys(selenium.webdriver.common.keys.Keys.RETURN)
# 只搜中标
zhongbiaoIcon = driver.find_element_by_xpath("//*[contains(text(), '招标结果')]")
if (not "active" in zhongbiaoIcon.get_attribute("class")):
    zhongbiaoIcon.click()

# 设定查询时间
print("手动选择时间，完成了之后输入enter")
input()


# startTimeInput = driver.find_element_by_id("starttime")
# startTimeInput.click()

# time.sleep(0.1)
# for c in starttime:
#     startTimeInput.send_keys(c)
# iframe = driver.find_elements_by_tag_name("iframe")[0]
# driver.switch_to.frame(iframe)
# dpOkInput = driver.find_element_by_id("dpOkInput")
# dpOkInput.click()
# driver.switch_to.default_content()

# endTimeInput = driver.find_element_by_id("endtime")
# endTimeInput.click()
# time.sleep(0.1)
# for c in endtime:
#     endTimeInput.send_keys(c)
# iframe = driver.find_elements_by_tag_name("iframe")[0]
# driver.switch_to.frame(iframe)
# dpOkInput = driver.find_element_by_id("dpOkInput")
# dpOkInput.click()
# driver.switch_to.default_content()

# timebut = driver.find_element_by_id("timebut")
# timebut.click()

# 获取所有item
print("开始获取页面内容")
all_items_data = []
df_all_data = None # Store all Zhongbiao information to this DataFrame

page_number = 0

while (True):
    page_number += 1

    all_items_data = full_page_information(driver, page_number, month)
    # Page save
    df_temp = pd.DataFrame(all_items_data)
    df_temp.to_csv(month + keywords + "page" + str(page_number) +".csv")

    next_page_button = driver.find_element_by_class_name("nbnext") 
    if (next_page_button.get_attribute("class") == "nbnext"):
        # it has next page
        next_page_button.click()
        driver.switch_to.window(driver.current_window_handle)
    else:
        break

df_temp.to_csv(month + keywords +".csv")
