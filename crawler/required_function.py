
# 数据清理
def content_cleaning(content):
    content = content.strip().replace("\'", "").replace('\'', '')
    return content

# 获取标题
def get_title(soup):
    title = ""
    try:
        span = soup.find('span', id="productTitle")
        title = span.text
    except AttributeError as attr_error:
        try:
            h1 = soup.find('h1', class_="_2IIDsE _3I-nQy")
            title = h1.text
        except AttributeError as attr_error:
            try:
                h1 = soup.find('h1', id="title")
                title = h1.find('span').text
            except Exception as error:
                print("Title Error", end=':')
                print(error)
        except Exception as error:
            print("Title Error", end=':')
            print(error)
    except Exception as error:
        print("Title Error", end=':')
        print(error)
    return content_cleaning(title)

# 获取上映时间
def get_release_time(soup):
    date = "0000.00.00"
    try:
        ul = soup.find('ul', attrs={"class": "a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"})
        li_list = ul.find_all('span', class_="a-text-bold")
        for li in li_list:
            if 'Release date' in li.text or 'Date First Available' in li.text:
                date = li.find_next('span').text
                break
        # print("method1: ", end='')
    except AttributeError as attr_error:
        try:
            date = soup.find('span', attrs={"data-automation-id": "release-year-badge"}).text
        except Exception as error:
            print("Date Error", end=':')
            print(error)
    return content_cleaning(date)

# 获取类型
def get_genre(soup):
    genre = ""
    try:
        tr = soup.find('tr', class_="a-spacing-small po-genre")
        td = tr.find('td', class_="a-span9")
        genre = td.find('span', class_="a-size-base").text
    except AttributeError as attr_error:
        try:
            div = soup.find('div', class_="_2KBC2m")
            dt_list = div.find_all('dt')
            for dt in dt_list:
                span = dt.find('span', class_="_36qUej")
                if "Genres" in span.text:
                    dd = dt.find_next('dd')
                    a_list = dd.find_all('a')
                    for a in a_list:
                        genre += a.text + ", "
                    break
        except Exception as error:
            print("Genre Error", end=':')
            print(error)
    except Exception as error:
            print("Genre Error", end=':')
            print(error)
    return content_cleaning(genre)

# 获取导演
def get_director(soup):
    director = ""
    try:
        ul = soup.find('ul', attrs={"class": "a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"})
        li_list = ul.find_all('span', class_="a-text-bold")
        for li in li_list:
            if 'Director' in li.text:
                director = li.find_next('span').text
                break
    except AttributeError as attr_error:
        # print(type(attr_error))
        try:
            div_list = soup.find_all('div', class_="_2KBC2m")
            for div in div_list:
                dt_list = div.find_all('dt')
                for dt in dt_list:
                    span = dt.find('span', class_="_36qUej")
                    if "Director" in span.text or "director" in span.text:
                        dd = dt.find_next('dd')
                        a_list = dd.find_all('a')
                        for a in a_list:
                            director += (a.text + ", ")
                        break
            temp = soup.find()
        except Exception as error:
            print("Direct Error", end=':')
            print(error)
    except Exception as error:
        print("Direct Error", end=':')
        print(error)
    return content_cleaning(director)

# 获取演员
def get_actors(soup):
    actors = ""
    try:
        ul = soup.find('ul', attrs={"class": "a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"})
        li_list = ul.find_all('span', class_="a-text-bold")
        for li in li_list:
            if 'Actor' in li.text:
                actors = li.find_next('span').text
                break
    except AttributeError as attr_error:
        try:
            div_list = soup.find_all('div', class_="_2KBC2m")
            for div in div_list:
                dt_list = div.find_all('dt')
                for dt in dt_list:
                    span = dt.find('span', class_="_36qUej")

                    if "Star" in span.text or "actor" in span.text or "star" in span.text:
                        dd = dt.find_next('dd')
                        a_list = dd.find_all('a')
                        for a in a_list:
                            actors += (a.text + ", ")
                        break
        except Exception as error:
            print("Actor Error", end=':')
            print(error)
    except Exception as error:
        print("Actor Error", end=':')
        print(error)    
    return content_cleaning(actors)