from xxlimited import new
from rapidfuzz import process
import pandas as pd
import requests, json

def movie_merge(movies_info: pd.DataFrame):
    all_columns = ('title', 'genre', 'release_date', \
        'actor', 'director', 'format', 'language')
    len_columns = ('title',)
    list_columns = ('genre', 'actor', 'director', 'format', 'language')
    date_columns = ('release_date',)
    time_columns = ('run_time',)
    
    # 数据血缘关系表
    data_related_table = pd.DataFrame(columns=list(len_columns + list_columns + date_columns))
    
    title_dict = {-1: ''} # 先放进去一个，以免第一次匹配时为None

    waiting_delete_list = []
    for index, row in movies_info.iterrows():
        title = row['title']
        title_value, score, old_index = process.extractOne(title, title_dict)
        if score > 95:
            waiting_delete_list.append(index) # 加入删除列表
            # print("waiting_delete_list_number={0}".format(len(waiting_delete_list)))
            # index和old_index是同一部电影，合并它们的字段
            new_attrs, old_attrs = movies_info.loc[index], movies_info.loc[old_index]
            print("{0} --> {1}".format(new_attrs['asin'], old_attrs['asin']))
            with open("./merge_log.txt", 'a') as log_file:
                log_file.write(
                    "{3}-{4}:\n {0} == {1} ==? {2}\n".format(
                        title_value, old_attrs['title'], 
                        new_attrs['title'],
                        len(waiting_delete_list), 
                        index,
                        )
                    )
            # 根据字符串长度合并
            for attr in len_columns:
                # 选取字段长的
                if pd.isna(new_attrs[attr]) or pd.isna(old_attrs[attr]) \
                or len(str(new_attrs[attr])) > len(str(old_attrs[attr])):
                    movies_info.loc[old_index, attr] = new_attrs[attr]
                    data_related_table.loc[old_index, attr] = 'https://www.amazon.com/-/en/dp/' + new_attrs['asin']

            for attr in list_columns:
                # 将相似度不高的列表数据合并
                new_list, old_list = new_attrs[attr], old_attrs[attr]
                # print("old_list=", movies_info.loc[old_index, attr])
                isAdded = False
                for item in new_list:
                    result = process.extractOne(item, old_list)
                    # print("result=", result)
                    if not result or result[1] <= 95: # 相似度不高才放入
                        old_list.append(item)
                        isAdded = True
                if isAdded:
                    movies_info.loc[old_index, attr] = old_list
                    new_asin_list = data_related_table.loc[old_index, attr] + ', https://www.amazon.com/-/en/dp/' + new_attrs['asin']
                    data_related_table.loc[old_index, attr] = new_asin_list
                # print("new_list=", movies_info.loc[old_index, attr])
            for attr in date_columns:
                # 维护oid_attrs[attr]不为空
                # 如果新的new_attrs[attr]不为空，则比较两者，选取时间更早的，并更改血缘关系
                temp_list = old_attrs[attr].split('-')
                try:
                    old_year, old_month, old_day = temp_list[0], temp_list[1], temp_list[2]
                    new_year, new_month, new_day = new_attrs[attr].split('-')
                    if new_year <= old_year or (new_month != 0 and new_month <= old_month) or (new_day != 0 and new_day < new_day):
                        movies_info.loc[old_index, attr] = new_attrs[attr]
                        data_related_table.loc[old_index, attr] = 'https://www.amazon.com/-/en/dp/' + new_attrs['asin']
                except Exception as error:
                    print(error)
            for attr in time_columns:
                # 时间选取更长的
                new_time, old_time = int(new_attrs[attr]), int(old_attrs[attr])
                if new_time != 0 or old_time != 0 or new_time > old_time:
                    movies_info.loc[old_index, attr] = new_attrs[attr]
                    data_related_table.loc[old_index, attr] = 'https://www.amazon.com/-/en/dp/' + new_attrs['asin']
        else:
            title_dict[index] = title # 标题放入字典
            new_series_dict = {'id': title}
            for attr in all_columns:
                new_series_dict[attr] = 'https://www.amazon.com/-/en/dp/' + row['asin'] # 全部来自一个asin产品
            if pd.isna(row['release_date']):
                url1 = 'https://imdb-api.com/API/SearchMovie/k_fjhihha0/' + title
                response = requests.get(url1)
                res_json = json.loads(response.text)
                movie_id = res_json.get('results')[0].get('id')
                url2 = 'https://imdb-api.com/en/API/Title/k_fjhihha0/' + movie_id
                response = requests.get(url2)
                movie_json = json.loads(response.text)
                release_date = movie_json.get('releaseDate')
                new_series_dict['release_date'] = url2
                movies_info.loc[index, 'release_date'] = release_date
            else:
                new_series_dict['release_date'] = 'https://www.amazon.com/-/en/dp/' + row['asin']
            new_df = pd.DataFrame(new_series_dict, index=[index])
            data_related_table = pd.concat([data_related_table, new_df])
        
    data_related_table.to_csv("../movies-information/related.csv")
    # log_file.close()
    return movies_info.drop(index=waiting_delete_list)


def merge_people_name(movies_info: pd.DataFrame):
    name_list = ['']
    for index, row in movies_info.iterrows():
        for attr in ('actor', 'director'):
            new_name_list = row[attr]
            # print(len(new_name_list))
            for name_index in range(len(new_name_list)):
                new_name = new_name_list[name_index]
                old_name, score, old_index = process.extractOne(new_name, name_list)
                if score > 95:
                    # 相同name进行替换，总是选择更长的name
                    # if len(new_name) > len(old_name):
                    #     name_list.remove(old_name)
                    #     name_list.append(new_name)
                    # else:
                    new_name_list[name_index] = old_name
                else:
                    name_list.append(new_name)
                    # if len(name_list) % 1000 == 0:
                    #     print(name_list)
            movies_info.loc[index][attr] = new_name_list
    # print(name_list)
    return movies_info