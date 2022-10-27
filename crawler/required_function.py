
# 数据清理
def content_cleaning(content):
    content = content.strip().replace("\"", "").replace('\'', '')
    return content

# 获取标题
def get_title(soup):
    title = ""
    try:
        span = soup.find('span', id="productTitle")
        title = span.text
    except Exception as error:
        # print("maybePV", end=', ')
        pass
    return content_cleaning(title)

def get_pv_title(asin, soup):
    title = ""
    global err
    try:
        h1 = soup.find('h1', class_="_2IIDsE _3I-nQy")
        title = h1.text
    except Exception as error:
        err = error
    try:
        h1 = soup.find('h1', id="title")
        title = h1.find('span').text
    except Exception as error:
        err = error
    if title == "":
        # print("Title Error", end=':')
        # print(err)
        with open("/Users/lc2002/Documents/2022-1/homework/DataWarehouse/crawler/unsolved-html.txt", 'a+') as f:
            f.write(asin + "\n")
    return title

def get_product_details_list(asin, soup):
    genre, release_date, first_available, actor, director, format, run_time, language = "", "", "", "", "", "", "", ""

    try:
        ul = soup.find('ul', class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list")
        li_list = ul.find_all('span', class_="a-text-bold")
        for li in li_list:
            if 'Genre' in li.text:
                genre = content_cleaning(li.find_next('span').text)
            elif 'Release date' in li.text:
                release_date = content_cleaning(li.find_next('span').text)
            elif 'Date First Available' in li.text:
                first_available = content_cleaning(li.find_next('span').text)
            elif 'Actor' in li.text:
                actor = content_cleaning(li.find_next('span').text)
            elif 'Director' in li.text:
                director = content_cleaning(li.find_next('span').text)
            elif 'Format' in li.text:
                format = content_cleaning(li.find_next('span').text)
            elif 'Run time' in li.text:
                run_time = content_cleaning(li.find_next('span').text)
            elif 'Language' in li.text:
                language = content_cleaning(li.find_next('span').text)
            # list_info_dict = {'Release date': release_date_1, 'Date First Available': first_available_1, 'actor': actor_1, 'director': director_1, 'format': format_1, 'run_time': run_time_1, 'language': language_1}
    # except AttributeError as attr_error:
    #     try:
    #         date = soup.find('span', attrs={"data-automation-id": "release-year-badge"}).text
    #     except Exception as error:
    #         print("Date Error", end=':')
    #         print(error)
    except Exception as error:
        with open("/Users/lc2002/Documents/2022-1/homework/DataWarehouse/crawler/unsolved-html.txt", 'a+') as f:
            f.write(asin + "\n")
        # print("info_list1 Error", end=':')
        # print(error)

    try:
        tb = soup.find('table', attrs={"class": "a-normal a-spacing-micro"})
        td_list = tb.find_all('span', class_="a-size-base a-text-bold")
        for td in td_list:
            if "Genre" in td.text:
                temp = content_cleaning(td.find_next('span').text)
                if len(genre) < len(temp):
                    genre = temp
            elif "Format" in td.text:
                temp = content_cleaning(td.find_next('span').text)
                if len(format) < len(temp):
                    format = temp
            elif "Language" in td.text:
                temp = content_cleaning(td.find_next('span').text)
                if len(language) < len(temp):
                    language = temp
            elif "Runtime" in td.text:
                temp = content_cleaning(td.find_next('span').text)
                if len(run_time) < len(temp):
                    run_time = temp
    except Exception as error:
        pass
    
    return [genre, release_date, first_available, actor, director, format, run_time, language]


def get_pv_product_details_list(soup):
    genre, release_date, first_available, actor, director, format, run_time, language = "", "", "", "", "", "", "", ""
    global err
    try:
        div_list = soup.find_all('div', class_="_2KBC2m")
        for div in div_list:
            dt_list = div.find_all('dt')
            for dt in dt_list:
                span = dt.find('span', class_="_36qUej") # 每个dt里面只有一个span，因此加不加class限定没有区别
                if "Director" in span.text:
                    dd = dt.find_next('dd')
                    a_list = dd.find_all('a')
                    for a in a_list:
                        director += a.text + ", "
                elif "Star" in span.text or "actor" in span.text:
                    dd = dt.find_next('dd')
                    a_list = dd.find_all('a')
                    for a in a_list:
                        actor += a.text + ", "
                elif "Genre" in span.text:
                    dd = dt.find_next('dd')
                    a_list = dd.find_all('a')
                    for a in a_list:
                        genre += a.text + ", "
                elif "language" in span.text:
                    dd = dt.find_next('dd')
                    language = dd.text
                elif "Format" in span.text:
                    dd = dt.find_next('dd')
                    span = dd.find('span', class_="_36qUej")
                    format = span.text
    except Exception as error:
        print("should not orror")
    
    run_time = get_pv_run_time(soup)
    release_date = get_pv_release_date(soup)

    return [genre, release_date, first_available, actor, director, format, run_time, language]

    
def get_pv_run_time(soup):
    run_time = ""
    try:
        span = soup.find('span', attrs={"data-automation-id": "runtime-badge"})
        run_time = span.text
    except Exception as error:
        # print("PV-runtime Error", end=":")
        # print(error)
        pass
    return run_time


def get_pv_release_date(soup):
    release_date = ""
    try:
        span = soup.find('span', attrs={"data-automation-id": "release-year-badge"})
        release_date = span.text
    except Exception as error:
        # print("PV-releasedate Error", end=":")
        # print(error)
        pass
    return release_date
