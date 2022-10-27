import pandas as pd

# 判断是否为电影
def isMovie(row: pd.Series):
    # 先判断时长
    run_time = int(row["run_time"])
    # print(type(run_time))
    if not pd.isna(run_time) and run_time != 0 and (run_time >= 400 or run_time <= 40):
        return False

    title_keyword = ['/', 'Exercise', 'PBS', 'CD', 'Analysis of', 'technique', 'Collection', 'teach', 'learn', 'instruct', 'Hollywood', 'Bollywood'] # Concert
    genre_keyword = ['Music Video', 'Concert', 'Special Interest', 'Exercise', 'Fitness', 'CD', 'documentary', 'series', 'BBC', 'episode', 'season']
    title = row['title']
    genre = row['genre']
    if not pd.isna(title):
        for kw in title_keyword:
            if kw in title:
                return False
    if not pd.isna(genre):
        for kw in genre_keyword:
            if kw in genre:
                return False
    return True

# 清理电影
def movies_filter(movies_info: pd.DataFrame):
    waiting_delete_index = []
    for index, row in movies_info.iterrows():
        # print("index = {0}".format(index))
        if not isMovie(row):
            waiting_delete_index.append(index)
    # print(len(waiting_delete_index))
    return movies_info.drop(index=waiting_delete_index)