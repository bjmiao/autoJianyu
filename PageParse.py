import selenium 
import seleniumrequests
from seleniumrequests import Chrome
import time
import os
from bs4 import BeautifulSoup
import pickle
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from urllib import parse

# from Parse import parse_page
def parse_page(soup):
    print("Parsing page...")
    data = {}
    # soup = BeautifulSoup(text)

    td_list = soup.find_all("td")
    td_text = [x.text for x in soup.find_all("td")]
    data = {}
    # # get all td:
    # find id 省份
    # next = 省份
    keywords_list = ["省份", "城市", "采购单位", "中标单位", "中标金额(元)", "项目名称"]
    for key in keywords_list:
        if key in td_text:
            key_index = td_text.index(key)
            # print(key_index)
            # print(td_list[key_index+1])
            sub_div_list = td_list[key_index+1].find_all("div")
            if (len(sub_div_list)>0):
                key_value = sub_div_list[0].text
            else:
                key_value = td_list[key_index+1].text
            print(key, key_value)
            data[key] = key_value

    try:
        # url_start = response.text.find("originalUrl")
        # start_quote = response.text.find('"', url_start)
        # end_quote = response.text.find('"', start_quote+1)
        # url = response.text[start_quote+1 : end_quote]
        url = soup.find("a", class_="com-original")['datahref']
        true_url = parse.parse_qs(parse.urlparse(url).query)['url']
        data['链接地址'] = true_url
    except Exception as e:
        print("Something wrong")
    # soup.find_all('a', class_="com-original")
    # keyword_mapping = {"省份":"省份","城市":"地市","采购单位":"采购人","中标单位":"实际集成商","中标金额(元)":"中标金额"
    # data = {"地市":"aaa", "项目类型":"bbb", "采购人":"ccc", "中标金额": 1000, "实际集成商":"fff",'中标集成商':"None"}
    return data


def full_page_information(driver, page_number, month):
    all_items_data = []
    items = driver.find_elements_by_class_name("liLuceneList")
    print("Page %d has %d items" % (page_number, len(items)))
    for item in items:
        # print(driver.window_handles)
        print(item)
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

        item_detail_link = item.find_element_by_class_name("left-title").find_element_by_tag_name('a')
        item_detail_link.click()

        # detail_page_base_url = "https://www.jianyu360.com/article/content/"
        # detail_page_url = detail_page_base_url + data_id + ".html"
        detail_data = None
        while (True):
            try:
                # response = driver.request("GET", detail_page_url)
                # status_code = response.status_code
                # if (status_code < 200 or status_code >= 300):
                    # raise Exception("Page not found")
                current_window = driver.current_window_handle
                driver.switch_to.window(driver.window_handles[0])
                driver.switch_to.window(driver.window_handles[-1])
        
                text = None
                while True:
                    # time.sleep(2)
                    text = driver.find_element_by_tag_name("html").get_attribute("outerHTML")
                    # # 判断
                    # f = open("test.html",'w', encoding="utf-8")
                    # f.write(text)
                    # f.close()
                    # pdb.set_trace()
                
                    break
                
                soup = BeautifulSoup(text)
                if ("验证码" in soup.title.text):
                    raise Exception("验证码输入")
                detail_data = parse_page(soup)
                item_data.update(detail_data)
                break
            except Exception as e:
                print("错误：", e)
                # js = 'window.open("http://www.baidu.com")'
                # driver.execute_script(js)
                # driver.get()
                print("输入验证码，完成后按enter键")
                input()
                # item_detail_link.click()

        driver.switch_to.window(driver.window_handles[0])

        # time.sleep(3)
        print(item_data)
        all_items_data.append(item_data.copy())

    return all_items_data



# df_all_data.to_csv("test.csv")