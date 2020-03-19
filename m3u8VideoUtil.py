from m3u8Parse import M3U8
from videoUtil import VideoUtil
import re


class M3U8VideoUtil(VideoUtil):
    def __init__(self, path):
        super().__init__()
        self.m3u8_path = path
        self.m3u8_parser = M3U8(self.m3u8_path)
        self.m3u8_parser_data = self.m3u8_parser.data()

    @staticmethod
    def is_url(url):
        r = re.compile('^https|http|ftp|hdfs?:/{2}\\w.+$')
        return re.match(r, url) is not None

    def m3u8_loader(self, url):
        if not self.m3u8_parser.exists():
            self.m3u8_parser.download(url)

    def get_m3u8_urls(self):
        return self.m3u8_parser_data.get("urls")

    def get_m3u8_file_names(self):
        urls = self.get_m3u8_urls()
        return [url[url.rfind('/') + 1:] for url in urls]

    def win_m3u8_reduce(self, file_dir,  file_path, group_reduce_num=200):
        path = self.get_m3u8_file_names()
        return self.win_reduce(file_dir, path, file_path, group_reduce_num)

    def ffmpeg_m3u8_reduce(self, file_dir, file_path):
        path = self.get_m3u8_file_names()
        return self.ffmpeg_reduce(file_dir, path, file_path)


if __name__ == '__main__':
    # M3U8VideoUtil().ffmpeg_m3u8_reduce('E:/download2/', 'E:/download2/output.m3u8', 'E:/success.mkv')
    pass
