import selenium 
import seleniumrequests
from seleniumrequests import Chrome
import time
import os
from bs4 import BeautifulSoup
# from Parse import parse_page
def parse_page(response):
    print("Parsing page...")
    data = {}
    soup = BeautifulSoup(response.text)

    td_text = [x.text for x in soup.find_all("td")]

    data = {}
    # # get all td:
    # find id 省份
    # next = 省份
    keywords_list = ["省份", "城市", "采购单位", "中标单位", "中标金额(元)"]
    for key in keywords_list:
        if key in td_text:
            key_index = td_text.index(key)
            key_value = td_text[key_index+1]
            print(key_index)
            print(key_value)
            data[key_index] = data[key_value]

    try:
        url_start = soup.text.find("originalUrl")
        start_quote = soup.text.find('"', url_start)
        end_quote = soup.text.find('"', start_quote+1)
        url = soup.text[start_quote+1 : end_quote]
        data['链接地址'] = url
    except Exception as e:
        print("Something wrong")
    # soup.find_all('a', class_="com-original")
    # keyword_mapping = {"省份":"省份","城市":"地市","采购单位":"采购人","中标单位":"实际集成商","中标金额(元)":"中标金额"
    # data = {"地市":"aaa", "项目类型":"bbb", "采购人":"ccc", "中标金额": 1000, "实际集成商":"fff",'中标集成商':"None"}
    return data

NOW_PATH = os.getcwd()

# 开始前，先把chromedriver.exe放到当前文件夹下

# 完成登录
driver = Chrome()
driver.request("POST", "https://www.jianyu360.com/phone/login", 
            data={"reqType" : "phoneLogin","phone" : "13166301938","password" : "123456"})
driver.get("https://www.jianyu360.com/jylab/supsearch/index.html")

keywords = "立体化 防控"
starttime = "20200501"
endtime = "20200531"

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
all_items = []


df_all_data = None # Store all Zhongbiao information to this DataFrame

while (True):
    items = driver.find_elements_by_class_name("liLuceneList")
    print("This page has %d items" % len(items))

    for item in items:
        all_items.append(item.get_attribute("innerHTML"))
        title = item.find_element_by_class_name("left-title").text
        tag_link = item.find_elements_by_tag_name('a')
        day = item.find_element_by_class_name("com-time").text
        data_id  = tag_link[0].get_attribute('dataid')
        tags = [x.text for x in tag_link[1:]]
        if not ('中标' in tags or '成交' in tags):
            continue
        # 项目名称，地点、项目类型、采购人、中标时间，中标金额，中标集成商，中标厂商和厂商金额
        print(title, data_id, tags)
        item_data = {"项目名称":title, "中标公布日":day}
        detail_page_base_url = "https://www.jianyu360.com/article/content/"
        detail_page_url = detail_page_base_url + data_id + ".html"
        detail_data = None
        try:
            response = driver.request("GET", detail_page_url)
            status_code = response.status_code
            if (status_code < 200 or status_code >= 300):
                raise Exception("Page not found")
            detail_data = parse_page(response)
            item_data.update(detail_data)
        except Exception as e:
            print("Page not found")
            continue

        print(item_data)
        # break        
        # （TODO) store item_data as a row of DataFrame

    # (TODO) Check next page
    next_page_button = "nbnext"
    # 
    # break

# df_all_data.to_csv("test.csv")