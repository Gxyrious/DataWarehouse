import pandas as pd
import re, locale
from datetime import datetime

def value_cleaner(movies_info: pd.DataFrame):
    movies_info.fillna(value='', inplace=True)
    for attr in ('title', 'genre', 'actor', 'director', 'format', 'language', 'release_date', 'first_available_date', 'run_time'):
        movies_info[attr] = remove_special_characters(movies_info[attr])

    return movies_info

def convert_to_list(list_str: str):
    new_list = list(map(lambda list_str: list_str.strip(), list_str.split(',')))
    while '' in new_list:
        new_list.remove('')
    return new_list

def date_cleaner(date_str: str):
    if date_str == '':
        pass
    elif date_str.isdigit():
        date_str = '{}-00-00'.format(date_str)
    else:
        try:
            locale.setlocale(locale.LC_ALL, 'en_us')
            date_str = str(datetime.strptime(date_str, '%B %d, %Y').date())
        except Exception as error:
            print(error)
    return date_str


def runtime_cleaner(runtime: str):
    hour, minute, second = 0, 0, 0
    try:
        runtime_list = runtime.split(' ')
        for index in range(len(runtime_list)):
            item = runtime_list[index]
            if item.isalpha():
                if 'hour' in item or 'h' == item: # 'hour' in 'hours'
                    hour = int(runtime_list[index - 1])
                elif 'minute' in item or 'min' == item: # 'minute' in 'minutes'
                    minute = int(runtime_list[index - 1])
            else:
                alphas = re.search(r'[a-zA-Z]+', item)
                numbers = re.search(r'[0-9]+', item)
                if alphas and numbers:
                    alphas = alphas.group()
                    numbers = int(numbers.group())
                    if 'min' in alphas:
                        minute = numbers
                    elif 'h' in alphas:
                        hour = numbers
                    elif 'sec' in alphas:
                        second = numbers
    except Exception as error:
        # print(runtime)
        pass
    return str(hour * 60 + minute + second // 60)


def title_cleaner(target: pd.Series):
    # title
    target = remove_brackets(target)
    target = remove_special_characters(target)
    return target


def language_cleaner(target: pd.Series):
    target = target.fillna(value="")
    target = remove_brackets(target)
    target = remove_special_characters(target)
    return target


def remove_special_characters(target: pd.Series):
    # 删除替换不规范字符
    target = target.apply(lambda c: c.encode('utf-8').decode())
    target = target.apply(
        lambda c: re.sub(r"‘|’|”|“", "'", c).strip()
    )
    target = target.apply(
        lambda c: re.sub(r"\n|\r|'\n|'\r", "", c).strip()
    )
    target = target.apply(
        lambda c: c.strip()
    )
    return target


def remove_brackets(target: pd.Series):
    target = target.apply(
        lambda c: re.sub(r"\(.*?\)|\{.*?}|\[.*?]", "" , c)
        )
    target = target.apply(
        lambda c: re.sub(r"\(.*?$|\{.*?$|\[.*?$", "" , c)
        )
    target = target.apply(
        lambda c: re.sub(r"\)|\]|\}", "", c)
    )
    return target
