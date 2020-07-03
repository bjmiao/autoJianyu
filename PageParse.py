import selenium 
import seleniumrequests
from seleniumrequests import Chrome

import os
NOW_PATH = os.getcwd()

# 开始前，先把chromedriver.exe放到当前文件夹下

# 完成登录
driver = Chrome()
# driver.get("http://www.python.org")
driver.request("POST", "https://www.jianyu360.com/phone/login", 
            data={"reqType" : "phoneLogin","phone" : "13166301938","password" : "123456"})
driver.get("https://www.jianyu360.com/jylab/supsearch/index.html")


# 填充搜索框
keywords = "立体化 防控"
searchInput = driver.find_element_by_id("searchinput")
searchInput.send_keys(keywords)
searchInput.send_keys(selenium.webdriver.common.keys.Keys.RETURN)