from threading import Thread
from multiprocessing import Process
from requests import get
from http.client import HTTPException
from calDisplayFormat import CalDisplayFormat
from os.path import exists
from os.path import getsize
from sys import stdout
from item import Item


class Download(object):
    headers = {
        "User-Agent": "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) "
                      "Version/8.0 Mobile/10A5376e Safari/8536.25 ",
        "Charset": "UTF-8",
        "Connection": "Keep-Alive",
        "Accept": "*/*",
    }
    existed_size = 0
    file_size = 0
    speed = 1024
    timeout = 3
    status = [200, 206]
    again = False
    res = False
    item = Item()
    log_name = "test"

    def __init__(self, url, path):
        super().__init__()
        self.url = url
        self.path = path

    def __change(self, key, val):
        if self.__getattribute__(key) != val:
            self.__setattr__(key, val)
        return val

    def add_header(self, key, val) -> None:
        self.headers[key] = val

    def check(self) -> None:
        if exists(self.path):
            self.existed_size = getsize(self.path)

    def over(self) -> bool:
        return self.existed_size == self.file_size

    def condition(self) -> bool:
        return self.item.check(self.log_name, self.url, str(True))

    def show(self) -> None:
        print("\n")
        print("--------------------------------------------------")
        print("下载地址 -> {}".format(self.url))
        print("文件位置 -> {}".format(self.path))
        print("文件大小 -> {}".format(self.file_size))
        print("文件下载完毕 ^~^")

    def run(self) -> bool:
        self.check()
        if self.condition():
            return self.__change("res", True)
        self.add_header("Range", "bytes={}-".format(str(self.existed_size + 1 if self.again else 0)))

        web_log = get(self.url, stream=True, headers=self.headers, timeout=self.timeout)
        if web_log.status_code in self.status:
            self.file_size = int(dict(web_log.headers).get('Content-Length'))

            if self.over():
                self.show()
                return self.__change("res", True)

            try:
                self.again = True if web_log.status_code == 206 else False
                with open(self.path, "ab" if self.again else "wb") as local_file:
                    for chunk in web_log.iter_content(chunk_size=self.speed):
                        if chunk:
                            local_file.write(chunk)
                            local_file.flush()
                            self.existed_size += len(chunk)
                            stdout.write("\r文件 [{}]  下载进度 -> {}".format(self.path,
                                                                        CalDisplayFormat().percent(self.existed_size,
                                                                                                   self.file_size)))
                            stdout.flush()
                    print("\n")
                    self.__change("res", self.existed_size == self.file_size)
            except HTTPException as err:
                print("下载错误 -> {}".format(repr(err)))

            return self.res


class Download_Thread(Download, Thread):
    pass


class Download_Process(Download, Process):
    pass


if __name__ == '__main__':
    # d = Download('http://120.241.192.212/vmtt.tc.qq.com/1098_c40a8cc1fe112c14a8f217134381b674.f0.mp4?vkey'
    #              '=4F129AE6DBC20EA0A5CCB61522816C3EEE52E61098382A06510FF74EC9106026A41B043ECB012559180950'
    #              'BE460AD86341F5153C65EA27E502406FB83CA325AE4DB8E743D6621E9DA3C4ED7F2DAF2F0BF717C24A0CA4C2F5',
    #              'E:/a.mp4')
    # d.start()
    pass
