import os
from downloadUtil import MultiDownload
from m3u8Parse import M3U8
from calTime import time_transfer


class M3U8DownloadLoader(object):
    def __init__(self, link=None, path='./download', sleep=5, d_type=0):
        self.link = link[:link.rfind('/')]
        self.path = self.set_download_path(path)
        self.sleep = sleep
        self.download_type = d_type
        self.m3u8_url = link
        self.m3u8_seed_name = link[link.rfind('/') + 1:]
        self.m3u8_path = "%s/%s" % (self.path, self.m3u8_seed_name)
        self.m3u8_parser = M3U8(self.m3u8_path)
        self.check_m3u8()
        self.m3u8_parser_data = self.m3u8_parser.data()
        self.total_video_time = sum(self.m3u8_parser_data.get("times"))
        self.total_video_format_time = time_transfer(self.total_video_time)

    # 设置文件下载路径
    @staticmethod
    def set_download_path(path):
        while not os.path.exists(path):
            os.mkdir(path)
        os.chdir(path)
        return path

    # 本地获取
    @staticmethod
    def get_local_file_size(file):
        return os.path.getsize(file)

    def check_m3u8(self):
        while not self.m3u8_parser.exists():
            self.m3u8_parser.download(self.m3u8_url)

    # 执行
    def start(self):
        self.check_m3u8()
        urls = self.m3u8_parser_data.get("urls")
        file_paths = [url[url.rfind('/') + 1:] for url in urls]
        file_num = len(file_paths)
        self.start_tips(file_num=file_num)
        MultiDownload(urls, file_paths).download(d_type=self.download_type, sleep=self.sleep)

    # 提示
    def start_tips(self, **kwargs):
        print('\n')
        print('==================================================')
        print('请求地址 -> {}'.format(self.m3u8_url))
        print('下载目录 -> {}'.format(self.path))
        print('m3u8位置 -> {}'.format(self.m3u8_path))
        print('文件数量 -> {}'.format(kwargs.get('file_num')))
        print('播放时长 -> {}'.format(self.total_video_format_time))
        print('==================================================')
        print('\n')
        print('准备下载，资源 Loding......')
        print('\n')


if __name__ == '__main__':
    """
    md = M3U8DownloadLoader(m3u8文件网址, m3u8文件下载位置)
    md.start()
    md.win_reduce_ts(r'E:/ts/', r'E:/ts/2.ts ')
    m.ffmpeg_reduce('E:/ts/ ', 'E:/ts/2.ts ')
    """

    # print('=========================================================')
    # seed_url = input('请输入m3u8文件地址：')
    # save_path = input('请输入m3u8视频文件的保存目录：')
    # sleep = int(input('请输入重新下载的停顿秒数：'))
    # d_type = int(input('请输入下载类型编号：\n 0 多线程 \n 1 多进程 \n'))
    # print('=========================================================')
    #
    # m = M3U8DownloadLoader(
    #     link=seed_url,
    #     path=save_path,
    #     sleep=sleep,
    #     d_type=d_type
    # )
    # m.start()
    #
    # print('=========================================================')
    # save_reduce_path = input('请输入文件合并后的保存位置：')
    # print('=========================================================')
    # m.ffmpeg_reduce(save_path, save_reduce_path)
    pass
