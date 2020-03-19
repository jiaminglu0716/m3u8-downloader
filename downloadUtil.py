from userAgent import UserAgent
from multiprocessing import Pool
from threading import Thread
from threading import Lock
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request
from urllib.request import urlopen
from calTime import CalTime
from calTime import time_transfer
from byteTransfer import ByteTransfer
from calDisplayFormat import CalDisplayFormat
from item import Item
import time
import os
import sys


class Download(Item, CalTime, ByteTransfer, CalDisplayFormat):
    status = [200, 206]
    req_1_status = 0
    req_2_status = 0
    result = False
    size = 0
    file_size = 0
    error = "None"
    log_name = "test"

    def __init__(self, link, file_path, speed=1024, timeout=5):
        super(Item, self).__init__()
        super(CalTime, self).__init__()
        super(ByteTransfer, self).__init__()
        super(CalDisplayFormat, self).__init__()
        self.link = link
        self.file_path = file_path
        self.speed = speed
        self.timeout = timeout

    def __set_res(self, item):
        self.__setattr__("res", item)

    def __get_res(self):
        return self.__getattribute__("res")

    def __res_tail(self):
        lent = 0
        while lent < self.size:
            self.__get_res().read(self.speed)
            lent += self.speed

    def __request(self, **kwargs):
        req = Request(url=self.link, method='GET')
        req.add_header('Accept', '*/*')
        req.add_header('Charset', 'UTF-8')
        req.add_header('Connection', 'Keep-Alive')
        req.add_header('User-Agent', UserAgent().get_random())
        if not kwargs.get('headers') is None:
            for (k, y) in kwargs.get('headers').items():
                req.add_header(k, y)
        return urlopen(req, timeout=self.timeout)

    def __file_save(self, mode='wb', existed_size=0):
        f = self.__get_res()
        fp = open(self.file_path, mode)
        fp.seek(existed_size)
        self.start()

        try:
            while self.size < self.file_size:
                data = f.read(self.speed)
                fp.write(data)
                self.size += len(data)
                self.end()
                speed = self.byte_speed(self.size, self.last_time()) if self.last_time() >= 1 else 0
                w_time = (self.last_time() * (self.file_size - self.size)) / self.size
                sys.stdout.write("%sprocess -> %s %s %s" % ("\r", self.percent(self.size, self.file_size), speed,
                                                            time_transfer(w_time)))
                sys.stdout.flush()
        except Exception as e:
            self.error = repr(e)
            print(self.error, "internal")

        self.end()
        sys.stdout.write("\n")
        f.close()
        fp.close()

    def tips(self):
        sys.stdout.write("url -> %s \n" % self.link)

    def condition(self):
        self.tips()
        return self.check(self.log_name, self.link, str(True))

    # Range: bytes=10- 206
    def run(self):
        if self.condition():
            print(self.link)
            print('okay')
            self.result = True
            return self.result

        f = self.__request()
        self.__set_res(f)

        if f.status in self.status:
            self.file_size = int(dict(f.headers).get('Content-Length', 0))
            self.req_1_status = f.status

            if os.path.exists(self.file_path):
                self.size = os.path.getsize(self.file_path)

                if self.size < self.file_size:
                    fd = self.__request(headers={"Range": "bytes = {}-".format(self.size + 1)})
                    self.req_2_status = fd.status

                    if self.req_2_status == 206:
                        print(fd.info().getheader('Content-Type'))
                        f.close()
                        self.__set_res(fd)
                        self.__file_save('ab', self.size)
                    elif self.req_2_status == 200:
                        self.__res_tail()
                        self.__file_save('ab', self.size)
                elif self.size > self.file_size:
                    self.__file_save()
            else:
                self.__file_save()

        self.result = (self.size == self.file_size)
        return self.result

    def save(self):
        if not self.result:
            self.add("ERROR!", self.error)
            self.add('url', self.link)
            self.add('request_1_status', self.req_1_status)
            self.add('request_2_status', self.req_2_status)
            self.add('file_size', self.byte_s(self.num(self.size)))
            self.add('total_size', self.byte_s(self.num(self.file_size)))
            self.add('time', self.last_time())
            self.add('file_name', self.file_path)
            self.add('result', self.result)
            self.save_log(self.log_name)


class Download_Thread(Download, Thread):
    pass


class Download_Process(Download, Process):
    pass


class MultiDownload(object):
    failed = []
    failed_file_paths = []
    lock: Lock

    def __init__(self, urls, file_paths, num=10):
        self.urls = urls
        self.file_paths = file_paths
        self.num = num

    def downloader(self, d_type):
        if d_type == 0:
            return ThreadPoolExecutor(max_workers=self.num)
        elif d_type == 1:
            return Pool(processes=self.num)  # 进程池中从无到有创建三个进程,以后一直是这三个进程在执行任务

    @staticmethod
    def download_obj(url, path, d_type):
        if d_type == 0:
            return Download_Thread(url, path)
        elif d_type == 1:
            return Download_Process(url, path)

    def download(self, sleep=5, d_type=0):
        p = self.downloader(d_type)

        if d_type == 0:
            self.lock = Lock()

        for index, url in enumerate(self.urls):
            d_obj = self.download_obj(url, self.file_paths[index], d_type)
            try:
                if d_type == 0:
                    self.lock.acquire(timeout=5)
                    res = p.submit(d_obj.run)
                    self.download_result(url, self.file_paths[index], res.result())
                    self.lock.release()
                elif d_type == 1:
                    """
                    from multiprocessing import process
                    这里暂时关闭了process文件里的某个报错，详情看该文件中文叙述
                    """
                    res = p.apply_async(d_obj.run)
                    # 异步运行，根据进程池中有的进程数，每次最多3个子进程在异步执行
                    # 返回结果之后，将结果放入列表，归还进程，之后再执行新的任务
                    # 需要注意的是，进程池中的三个进程不会同时开启或者同时结束
                    # 而是执行完一个就释放一个进程，这个进程就去接收新的任务。
                    self.download_result(url, self.file_paths[index], res.get())
                d_obj.save()
            except Exception as e:
                """
                Exception Types:
                1. URLError
                """
                self.failure(url, self.file_paths[index])
                print(repr(e), "external")

        # 异步apply_async用法：如果使用异步提交的任务，主进程需要使用jion，等待进程池内任务都处理完，然后可以用get收集结果
        # 否则，主进程结束，进程池可能还没来得及执行，也就跟着一起结束了
        if d_type == 1:
            p.close()
            p.join()
        # for res in res_list:
        #     print(res.get())  # 使用get来获取apply_aync的结果,如果是apply,则没有get方法,因为apply是同步执行,立刻获取结果,也根本无需get
        if not len(self.failed) == 0:
            print('{} 个文件下载失败, {} 秒后准备重新下载'.format(len(self.failed), str(sleep)))
            time.sleep(sleep)
            self.re_download(d_type)
        else:
            print("All Missions Completed")

    def download_result(self, url, file_path, success):
        if success:
            print(" [ %s ] -> Success " % file_path)
        else:
            print(" [ %s ] -> Failure " % file_path)
            self.failure(url, file_path)

    def failure(self, url, file_path):
        self.failed.append(url)
        self.failed_file_paths.append(file_path)

    def failure_clear(self):
        self.failed_file_paths = []
        self.failed = []

    def failure_reset(self, reset=True):
        self.file_paths = self.failed_file_paths
        self.urls = self.failed

        if reset:
            self.failure_clear()

    def re_download(self, d_type):
        self.failure_reset()
        self.download(d_type=d_type)


if __name__ == '__main__':
    # print(datetime.datetime.now())
    # # 格式化输出
    # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # print(datetime.datetime.today())
    # start = datetime.datetime.now()

    # end = datetime.datetime.now()
    # print("程序运行时间：" + str((end - start).seconds) + "秒")
    pass
