
'''
    单线程爬取start<=index<=end的网页
'''

import os
import numpy as np
from amazoncaptcha import AmazonCaptcha
from selenium import webdriver
from bs4 import BeautifulSoup

def read_with_certain_index(start, end, save_path):
    # 爬取[start, end]范围的网页
    productId_list = np.load('productId_list.npy')
    driver = webdriver.Safari()
    for index in range(start, end + 1):
        productId = productId_list[index]
        url='https://www.amazon.com/-/en/dp/' + productId
        driver.get(url)

        page_source = driver.page_source # 获取页面源代码
        
        try:
            soup = BeautifulSoup(page_source)
            img_src = soup.find(class_="a-row a-text-center").findChild(name="img").attrs["src"]
            captcha = AmazonCaptcha.fromlink(img_src)
            solution = captcha.solve(keep_logs=True)

            captcha_input = driver.find_element_by_id("captchacharacters")
            captcha_input.send_keys(solution)

            button = driver.find_element_by_class_name("a-button-text")
            button.click()
        except Exception as error:
            print("can't find captcha", error)

        # 保存页面源代码，该数据量较大，建议存放到外接硬盘
        f = open(os.path.join(save_path, "{0}.html".format(productId)), 'w', encoding="utf-8")
        f.write(page_source)
        f.close()