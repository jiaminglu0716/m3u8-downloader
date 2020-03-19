from m3u8 import M3U8DownloadLoader
from m3u8VideoUtil import M3U8VideoUtil


def download(data=False):
    print('=========================================================')
    seed_url = input('请输入m3u8文件地址: ').strip()
    save_path = input('请输入m3u8视频文件的保存目录: ')
    sleep = int(input('请输入重新下载的停顿秒数: '))
    d_type = int(input('请输入下载类型编号： 0 多线程  1 多进程: '))
    print('=========================================================')

    mdl = M3U8DownloadLoader(
        link=seed_url,
        path=save_path,
        sleep=sleep,
        d_type=d_type
    ).start()

    if data:
        return save_path, mdl.m3u8_path


def download_reduce():
    save_path, m3u8_path = download(data=True)

    print('=========================================================')
    reduce_file_path = input('请输入文件合并后的存储目录: ')
    reduce_file_name = input('请输入文件合并后的存储文件名: ')
    save_reduce_path = reduce_file_path + reduce_file_name
    print('=========================================================')

    M3U8VideoUtil(m3u8_path).ffmpeg_m3u8_reduce(save_path, save_reduce_path)


def reduce():
    print('=========================================================')
    save_path = input('请输入合并文件的目录: ')
    m3u8_path = input('请输入文件m3u8位置: ')
    reduce_file_path = input('请输入文件合并后的存储目录: ')
    reduce_file_name = input('请输入文件合并后的存储文件名: ')
    save_reduce_path = "%s/%s" % (reduce_file_path, reduce_file_name)
    print('=========================================================')
    M3U8VideoUtil(m3u8_path).ffmpeg_m3u8_reduce(save_path, save_reduce_path)


def use_mode(mode_n):
    if mode_n == 1:
        download_reduce()
    elif mode_n == 2:
        download()
    elif mode_n == 3:
        reduce()


if __name__ == '__main__':
    """
    如果用cmd安装插件可以试下：
    双击run.bat运行
    """
    print('请选择使用的模式：')
    print('1 下载并且合并')
    print('2 下载视频')
    print('3 合并视频')

    mode_s = input('模式: ')
    mode = int(mode_s)

    use_mode(mode)

    """
    下载视频
    """
    # url = ""
    # mdl = M3U8DownloadLoader(
    #     link=url,
    #     path="d:/download4",
    #     sleep=5,
    #     d_type=0
    # ).start()

    """
    合并视频
    """
    # M3U8VideoUtil('D:/download2/output.m3u8').ffmpeg_m3u8_reduce('D:/download2', 'D:/o2.ts')
