from tkinter import W
from rapidfuzz import process
import pandas as pd

def movie_merge(movies_info: pd.DataFrame):
    # log_file = open("./merge_log.txt", 'a')

    # 'asin', 'title', 'genre', 'release_data', 'first_available_date', 'actor', 'director', 'format', 'run_time', 'language'
    len_columns, list_columns, date_columns = ('title',), ('genre', 'actor', 'director', 'format', 'language'), ('release_date', 'first_available_date')

    title_dict = {-1: ''} # 先放进去一个，以免第一次匹配时为None

    waiting_delete_list = []
    for index, row in movies_info.iterrows():
        title = row['title']
        title_value, score, old_index = process.extractOne(title, title_dict)

        if score > 95:
            waiting_delete_list.append(index)
            print("waiting_delete_list_number={0}".format(len(waiting_delete_list)))

            # index和target_index是同一部电影，合并它们的字段
            new_attrs, old_attrs = movies_info.loc[index], movies_info.loc[old_index]
            with open("./merge_log.txt", 'a') as log_file:
                log_file.write("{3}-{4}:\n {0} == {1} ==? {2}\n".format(title_value, old_attrs['title'], new_attrs['title'], len(waiting_delete_list), index))
            # 根据字符串长度合并
            for attr in len_columns:
                if pd.isna(new_attrs[attr]) or \
                        not pd.isna(new_attrs[attr]) and pd.isna(old_attrs[attr]) or \
                        len(str(new_attrs[attr])) > len(str(old_attrs[attr])): # 选取字段长的
                    movies_info.loc[old_index, attr] = new_attrs[attr]

            for attr in list_columns:
                new_list, old_list = new_attrs[attr], old_attrs[attr]
                # print("old_list=", movies_info.loc[old_index, attr])
                for item in new_list:
                    result = process.extractOne(item, old_list)
                    # print("result=", result)
                    if not result or result[1] <= 95: # 相似度不高才放入
                        old_list.append(item)
                movies_info.loc[old_index, attr] = old_list
                # print("new_list=", movies_info.loc[old_index, attr])
        else:
            title_dict[index] = title
    # log_file.close()
    return movies_info.drop(index=waiting_delete_list)
