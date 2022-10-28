from rapidfuzz import process
import pandas as pd

def movie_merge(movies_info: pd.DataFrame):
    all_columns = ('title', 'genre', 'release_date', 'first_available_date', \
        'actor', 'director', 'format', 'run_time', 'language')
    len_columns = ('title',)
    list_columns = ('genre', 'actor', 'director', 'format', 'language')
    date_columns = ('release_date', 'first_available_date', 'run_time')
    
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
                    data_related_table.loc[old_index, attr] = new_attrs['asin']

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
                    new_asin_list = data_related_table.loc[old_index, attr] + ',' + new_attrs['asin']
                    data_related_table.loc[old_index, attr] = new_asin_list
                # print("new_list=", movies_info.loc[old_index, attr])
            for attr in date_columns:
                # 日期选取更早的、时间选取更长的
                # print("type:: ", end='')
                # print(old_attrs[attr], new_attrs[attr])
                pass
                
        else:
            title_dict[index] = title # 标题放入字典
            new_series_dict = {'id': title}
            for attr in all_columns:
                new_series_dict[attr] = row['asin'] # 全部来自一个asin产品
            new_df = pd.DataFrame(new_series_dict, index=[index])
            data_related_table = pd.concat([data_related_table, new_df])
        
    data_related_table.to_csv("/Users/lc2002/Documents/2022-1/homework/DataWarehouse/movies-information/related.csv")
    # log_file.close()
    return movies_info.drop(index=waiting_delete_list)
