
'''
    读取start<=index<=end的网页
'''
from main import read_with_certain_index
import threading
# start_index = 1
# end_index = 100000
# each_json_include_movie_number = 500
ejimn = 100 # 每个json存储多少条数据，

# start = 1
# end = 100000

start = 100001
end = 200000

# start = 200000
# end = 250000

thread_number = 10 # 并行爬取的线程数


# single_time = total_number // thread_number

if __name__ == "__main__":
    total_number = end - start + 1 # 爬取总数
    single_time = total_number // thread_number # 每个线程爬取的数目，需要保证能整除
    for index in range(thread_number):
        thread = threading.Thread(
            target=read_with_certain_index,
            args=(index + 1, start + index * single_time, start + (index + 1) * single_time, ejimn)
        ).start()
    # thread1 = threading.Thread(target=read_with_certain_index, args=(1, 1, 10, each_json_include_movie_number))
    # # read_with_certain_index(no=1, start=start_index, end=end_index, ejimn=)
    # thread2 = threading.Thread(target=read_with_certain_index, args=(2, 11, 20, each_json_include_movie_number))
    # thread3 = threading.Thread(target=read_with_certain_index, args=(3, 21, 30, each_json_include_movie_number))
    # thread1.start()
    # thread2.start()
    # thread3.start()
    print("ended!")