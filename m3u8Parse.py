import os
import requests


class M3U8(object):
    url: str
    url_path: str
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/67.0.3396.99 Safari/537.36 "
    }
    info = {
        "urls": [],
        "times": []
    }

    def __init__(self, path):
        self.path = path

    def __m3u8(self):
        return self.path.endswith(".m3u8")

    def __download_check(self):
        lines = self.read()
        with open(self.path, "w") as fp:
            for line in lines:
                if not line.startswith('#'):
                    if line.find('/') == -1:
                        line = self.url_join(self.url_path, line)
                fp.write("%s\n" % line)
            fp.close()

    def exists(self):
        return os.path.exists(self.path)

    def request(self, url):
        self.url = url
        self.url_path = url[0: url.rfind('/')]
        return requests.get(url, headers=self.headers)

    def download(self, url):
        res = self.request(url)
        if res.status_code == 200:
            with open(self.path, "wb") as fp:
                fp.write(res.content)
                fp.close()
            self.__download_check()

    def read(self):
        if self.__m3u8():
            if self.exists():
                lines = []
                with open(self.path, "r") as fp:
                    for line in fp.readlines():
                        lines.append(line[:line.rfind('\n')])
                    fp.close()
                return lines

    def data(self):
        lines = self.read()
        size_h = "#EXTINF:"
        for line in lines:
            if not line.startswith('#'):
                self.info["urls"].append(line)
            elif line.startswith(size_h):
                size = line[line.find(size_h) + len(size_h):line.rfind(',')]
                f_size = float(size)
                self.info["times"].append(f_size)
        return self.info

    @staticmethod
    def url_join(url, file_path):
        forth = str(url).endswith('/')
        after = str(file_path).startswith('/')

        if (forth and not after) or (not forth and after):
            r_url = str(url) + str(file_path)
        elif forth and after:
            r_url = str(url) + str(file_path)[1:]
        else:
            r_url = str(url) + '/' + str(file_path)

        return r_url

    def decode(self):
        pass


if __name__ == '__main__':
    # m = M3U8(path='D:/download3/output.m3u8')
    # m.download('')
    # print(len(m.data().get("urls")))
    pass
