from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
import sys, re, queue, threading


work = queue.Queue()
lock = threading.Lock()


class CustomThread(threading.Thread):
    def __init__(self, index, client):
        super().__init__()
        self.threadId = index
        # self.que = que_list
        self.client = client

    def run(self):
        print("开启线程:" + str(self.threadId))
        delete_index(self.client)
        print("结束线程:" + str(self.threadId))


def create_es_client():
    es = Elasticsearch(hosts=["https://elastic:Q123456q.@vpc-jaeger-pro-gvusrzggv76j2qoztqijyvpbci.ap-southeast-1.es.amazonaws.com"])
    return es


def get_all_indexes(client):
    indexes = list(client.indices.get_alias('*'))
    # print(indexes)
    """ 过滤出所要的key"""
    filter_date = (datetime.now() + timedelta(days=-3)).date()
    print(filter_date)
    lock.acquire()
    for index in indexes:
        print(index)
        result = re.match(r'.*\-(\d+\-\d+\-\d+)$', index)
        if result:
            fmt = result.group(1)
            print("format date string is", fmt)
            str_date = datetime.strptime(fmt, '%Y-%m-%d').date()
            if str_date <= filter_date:
                print("index is",index)
                work.put(index)
    lock.release()


def delete_index(client):
    # for index in indexes:
    #     try:
    #         client.indices.delete(index)
    #     except Exception as e:
    #         sys.stderr.write(str(e))
    #     else:
    #         sys.stdout.writable("操作完成")
    while work.qsize() > 0:
        lock.acquire()
        item = work.get()
        try:
            client.indices.delete(item)
        except Exception as e:
            sys.stderr.write(str(e))
        else:
            sys.stdout.write("操作完成")
        lock.release()


def job():
    client = create_es_client()
    get_all_indexes(client)
    for i in range(2):
        thread = CustomThread(i, client)
        thread.start()
        thread.join()

    print("退出主线程")


if __name__ == "__main__":
    job()
