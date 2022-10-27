
'''
    读取start<=index<=end的网页
'''
from read_with_certain_index import read_with_certain_index
import threading

# start = 0
# end = 99999

# start = 100000
# end = 199999

start = 200000
end = 249999

thread_number = 5 # 并行爬取的线程数

save_path = "/Volumes/bGxyrious/DW/WebPages"


# single_time = total_number // thread_number

if __name__ == "__main__":
    total_number = end - start + 1 # 爬取总数
    single_time = total_number // thread_number # 每个线程爬取的数目，需要保证能整除
    for index in range(thread_number):
        threading.Thread(
            target=read_with_certain_index,
            args=(start + index * single_time, start + (index + 1) * single_time, save_path - 1)
        ).start()

    print("ended!")