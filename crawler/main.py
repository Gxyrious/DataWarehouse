from amazoncaptcha import AmazonCaptcha
from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import os, json

from required_function import get_actors, get_director, get_genre, get_release_time, get_title


def read_with_certain_index(no, start, end, ejimn):
    productId_list = np.load('productId_list.npy')
    if not os.path.exists('./json/info-{0}'.format(no)):
        os.makedirs('./json/info-{0}'.format(no))
    print(len(productId_list))
    driver = webdriver.Safari()
    movie_info = {}
    for index in range(start, end + 1):

        single_info = {}
        productId = productId_list[index]
        # try:
        url='https://www.amazon.com/-/en/dp/' + productId
        driver.get(url)

        # 将源代码保存在本地
        page_source = driver.page_source # 获取页面源代码
        # 保存页面源代码，该数据量较大，建议存放到外接硬盘
        f = open("./html/{0}-{1}.html".format(index, productId), 'w', encoding="utf-8")
        f.write(page_source)
        f.close()
        soup = BeautifulSoup(page_source)

        # 获取信息 #
        # single_info = {}

        # 0.获取标题
        title = get_title(soup)
        single_info["title"] = title.replace('\"', '').replace('\'', '')
        # 1.获取date
        date = get_release_time(soup)
        single_info["date"] = date.replace('\"', '').replace('\'', '')

        # 2.获取genre
        genre = get_genre(soup)
        single_info["genre"] = genre.replace('\"', '').replace('\'', '')

        # 3.获取导演
        director = get_director(soup)
        single_info["director"] = director.replace('\"', '').replace('\'', '')

        # 4.获取演员
        actors = get_actors(soup)
        single_info["actors"] = actors.replace('\"', '').replace('\'', '')

        movie_info[productId] = single_info
        print("{0}-{1}-succeeded!!".format(index, productId), end='')
        print(str(single_info).replace("\'", "\""))
        # 能输出这个说明没有问题了
        if index % ejimn == 0:
            # print(index)
            with open("info-{1}/movies-{0}.json".format(index // ejimn, no), "w") as outfile:
                json.dump(movie_info, outfile)
            movie_info = {}
        # 5.获取验证码
        # img_src = soup.find(class_="a-row a-text-center").findChild(name="img").attrs["src"]
        # captcha = AmazonCaptcha.fromlink(img_src)
        # solution = captcha.solve(keep_logs=True)

        # captcha_input = driver.find_element_by_id("captchacharacters")
        # captcha_input.send_keys(solution)

        # button = driver.find_element_by_class_name("a-button-text")
        # button.click()
        # print("验证码-" + solution + " 输入完毕")
        # except AttributeError as attr_error:
            # print(attr_error,end='')
        # except Exception as error:
        #     print("{0}-{1}-error!!!".format(index, productId))
        #     print(error)