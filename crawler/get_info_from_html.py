
'''
    从爬取的html文件中获取电影信息
'''

import os
from bs4 import BeautifulSoup
from required_function import *
import pandas as pd

def get_info_from_html(root_path, start, end):
    movies_info_list = []
    file_name_list = os.listdir(root_path)
    print("start!")
    for index in range(start, end + 1):
        
        file_name = file_name_list[index]
    # for file_name in file_name_list:
        html_path = os.path.join(root_path, file_name)
        # 1.根据文件名获取asin
        asin = file_name.split('.')[0]
        # print(asin)
        single_movie_info_list = []
        try:
            with open(html_path) as file:
                source = file.read()
                soup = BeautifulSoup(source, features='lxml')
                # 获取各种数据
                # 2.获取标题
                movie_title = get_title(soup)
                if movie_title != "":
                    single_movie_info_list.append(asin)
                    single_movie_info_list.append(movie_title)
                    # 遍历Product details列表，获取：
                    # 3.风格genre
                    # 4.发布日期
                    # 5.首次可用日期
                    # 6.演员actor
                    # 7.导演director
                    # 8.格式format
                    # 9.运行时长run_time
                    # 10.语言language
                    product_details_list = get_product_details_list(asin, soup)
                    single_movie_info_list.extend(product_details_list)
                else:
                    # 如果获取不到，说明是PrimeVideo页面
                    movie_title = get_pv_title(asin, soup)
                    if movie_title == "":
                        continue
                    single_movie_info_list.append(asin)
                    single_movie_info_list.append(movie_title)
                    product_details_list = get_pv_product_details_list(soup)
                    single_movie_info_list.extend(product_details_list)
            movies_info_list.append(single_movie_info_list)
            if (index+1) % 100 == 0:
                print("====={}=====".format(index+1))
        except Exception as error:
            print(error)
            with open("/Users/lc2002/Documents/2022-1/homework/DataWarehouse/crawler/unsolved-html.txt", 'a+') as f:
                f.write(asin + "\n")
    return movies_info_list
            

def write_info_to_file(target_list, path):
    name = ["asin", "title", "genre", "release_data", "first_available_date", "actor", "director", "format", "run_time", "language"]
    csv_file = pd.DataFrame(columns=name, data=target_list)
    csv_file.to_csv(path)



if __name__ == "__main__":
    root_path = "/Volumes/bGxyrious/DW/WebPages"
    write_path = "/Users/lc2002/Documents/2022-1/homework/DataWarehouse/crawler/movies-info/movies-0w-24w.csv"
    movies_info_list = get_info_from_html(root_path, start=0, end=239999)

    write_info_to_file(movies_info_list, write_path)
