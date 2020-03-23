from userAgent import UserAgent
from multiprocessing import Pool, Process
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from calTime import CalTime, timestamp_to_date, time_transfer
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

    def __init__(self, link, file_path, speed=1024, timeout=5, used_mode=1):
        super(Item, self).__init__()
        super(CalTime, self).__init__()
        super(ByteTransfer, self).__init__()
        super(CalDisplayFormat, self).__init__()
        self.link = link
        self.file_path = file_path
        self.speed = speed
        self.timeout = timeout
        self.condition_res = self.condition()
        self.used_mode = used_mode

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
                display_item = self.show_item("process -> %s  %s  %s" % (self.percent(self.size, self.file_size), speed,
                                                                         time_transfer(w_time)))
                sys.stdout.write("%s%s" % ("\r", display_item))
                sys.stdout.flush()
        except Exception as e:
            """
            Exception Types:
            1. timeout('The read operation timed out')
            """
            self.error = repr(e)
            sys.stdout.write("\n{ %s } -> %s" % (self.error, "internal"))

        self.end()
        sys.stdout.write("\n")
        f.close()
        fp.close()

    def __file_check(self, f):
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

    def set_mode(self, num):
        self.used_mode = num

    def tips(self):
        sys.stdout.write(self.show_item("url -> %s \n" % self.link))

    def condition(self):
        self.tips()
        return self.check(self.log_name, self.link, str(True))

    # Range: bytes=10- 206
    def run(self):
        if self.condition_res:
            self.result = True
            return self.result

        if self.used_mode in [1, 2, 3]:
            f = self.__request()
            self.__set_res(f)

            if f.status in self.status:
                self.file_size = int(dict(f.headers).get('Content-Length', 0))
                self.req_1_status = f.status

                if self.used_mode == 1:
                    self.__file_check(f)

            self.result = (self.size == self.file_size)

        return self.result

    def show_item(self, item):
        return "[%s] %s" % (timestamp_to_date(self.now()), item)

    def save(self):
        # if self.condition_res is False:
        self.add("ERROR!", self.error)
        self.add('url', self.link)
        self.add('request_1_status', self.req_1_status)
        self.add('request_2_status', self.req_2_status)
        self.add('file_size', self.byte_s(self.num(self.size)))
        self.add('total_size', self.byte_s(self.num(self.file_size)))
        self.add('file_name', self.file_path)
        self.add('result', self.result)
        self.save_log(self.log_name)


class Download_Thread(Download, Thread):
    pass


class Download_Process(Download, Process):
    pass


class MultiDownload(CalTime):
    failed = []
    failed_file_paths = []
    lock: Lock
    download_again = True
    result: bool

    def __init__(self, urls, file_paths, num=10, d_type=0, sleep=5):
        super(CalTime, self).__init__()
        self.urls = urls
        self.file_paths = file_paths
        self.num = num
        self.d_type = d_type
        self.sleep = sleep

    def set_download_again(self, res):
        self.download_again = res

    def downloader(self):
        if self.d_type == 0:
            return ThreadPoolExecutor(max_workers=self.num)
        elif self.d_type == 1:
            return Pool(processes=self.num)  # 进程池中从无到有创建三个进程,以后一直是这三个进程在执行任务

    def download_obj(self, url, path, mode):
        if self.d_type == 0:
            return Download_Thread(url, path, used_mode=mode)
        elif self.d_type == 1:
            return Download_Process(url, path, used_mode=mode)

    def download(self, mode=1):
        p = self.downloader()
        if self.d_type == 0:
            self.lock = Lock()
        self.start()

        for index, url in enumerate(self.urls):
            d_obj = self.download_obj(url, self.file_paths[index], mode)
            try:
                if self.d_type == 0:
                    self.lock.acquire(timeout=5)
                    res = p.submit(d_obj.run)
                    self.result = res.result()
                    self.lock.release()
                elif self.d_type == 1:
                    """
                    from multiprocessing import process
                    这里暂时关闭了process文件里的某个报错，详情看该文件中文叙述
                    """
                    res = p.apply_async(d_obj.run)
                    # 异步运行，根据进程池中有的进程数，每次最多3个子进程在异步执行
                    # 返回结果之后，将结果放入列表，归还进程，之后再执行新的任务
                    # 需要注意的是，进程池中的三个进程不会同时开启或者同时结束
                    # 而是执行完一个就释放一个进程，这个进程就去接收新的任务。
                    self.result = res.get()
                self.download_result(url, self.file_paths[index], self.result, mode)
            except Exception as e:
                """
                Exception Types:
                1. URLError(timeout('_ssl.c:1091: The handshake operation timed out'))
                2. URLError(gaierror(11001, 'getaddrinfo failed'))
                3. timeout('The read operation timed out')
                4. ConnectionResetError(10054, '远程主机强迫关闭了一个现有的连接。', None, 10054, None)
                """
                self.failure(url, self.file_paths[index])
                sys.stdout.write("{ %s } -> %s\n" % (repr(e), "external"))
            if mode in [1, 3]:
                d_obj.save()
        # 异步apply_async用法：如果使用异步提交的任务，主进程需要使用json，等待进程池内任务都处理完，然后可以用get收集结果
        # 否则，主进程结束，进程池可能还没来得及执行，也就跟着一起结束了
        if self.d_type == 1:
            p.close()
            p.join()
        # for res in res_list:
        #     print(res.get())  # 使用get来获取apply_async的结果,如果是apply,则没有get方法,因为apply是同步执行,立刻获取结果,也根本无需get
        self.task_result()

    def download_result(self, url, file_path, success, mode=1):
        if mode == 1:
            self.download_result_print(file_path, success)
        if not success:
            self.failure(url, file_path)

    def download_result_print(self, file_path, success):
        if success:
            sys.stdout.write(self.show_item("[ %s ] -> Success" % file_path))
        else:
            sys.stdout.write(self.show_item("[ %s ] -> Failure" % file_path))

    def task_result(self):
        if not len(self.failed) == 0:
            self.end()
            print("%d 个文件下载失败, %d 秒后准备重新下载" % (len(self.failed), self.sleep))
            print("总时长 -> %s" % time_transfer(self.last_time()))
            if self.download_again:
                time.sleep(self.sleep)
                self.re_download()
        else:
            self.end()
            print("All Missions Completed")
            print("完成时长 -> %s" % time_transfer(self.last_time()))

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

    def re_download(self):
        self.failure_reset()
        self.download(mode=1)

    def check_uncompleted_task(self):
        self.download(mode=3)
        return self.failed, self.failed_file_paths

    def continue_download(self):
        # check urls and add url in task list
        self.check_uncompleted_task()
        # now, we begin to download these urls in our task list
        self.re_download()

    def show_item(self, item):
        return "[%s] %s\n" % (timestamp_to_date(self.now()), item)


if __name__ == '__main__':
    """
    use_mode:
    0   check file in local log
    1   download
    2   check file in internet
    3   check file in internet and save result in local log
    """
    pass
