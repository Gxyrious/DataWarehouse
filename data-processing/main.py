import os
import pandas as pd
from data_cleaner import *
from movie_filter import *
from movie_merge import *

def read_csv_data(path):
    df = pd.read_csv(path, index_col=0)
    return df

def write_csv_data(df, path):
    df.to_csv(path)


if __name__ == "__main__":
    # 先读取csv文件，去除多余的Unname 0列（在保存csv文件时）
    root_path = "../movies-information"
    read_path = os.path.join(root_path, "movies-0w-24w.csv")
    write_path = os.path.join(root_path, "v5-merge_movies.csv")

    # 读取csv文件
    movies_info = read_csv_data(read_path)

    # 处理运行时长
    movies_info["run_time"] = movies_info["run_time"].apply(runtime_cleaner)

    # 删除非电影部分
    movies_info = movies_filter(movies_info)
    
    # 处理电影标题
    movies_info['title'] = title_cleaner(movies_info['title'])

    # 处理语言
    movies_info['language'] = language_cleaner(movies_info['language'])

    # 处理各种信息（待写）
    movies_info = value_cleaner(movies_info)
    
    # 转换为list
    for attr in ('genre', 'actor', 'director', 'format', 'language'):
        movies_info[attr] = movies_info[attr].apply(convert_to_list)
    
    # 处理相同演员
    movies_info  = merge_people_name(movies_info)

    # 日期标准化
    for attr in ('release_date', 'first_available_date'):
        movies_info[attr] = movies_info[attr].apply(date_cleaner)

    # 合并相同电影
    movies_info = movie_merge(movies_info)

    # 写csv数据
    write_csv_data(movies_info, write_path)
    