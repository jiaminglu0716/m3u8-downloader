import os


class VideoUtil(object):
    def __init__(self):
        pass

    @staticmethod
    def video_type(path, v_type):
        return path.endswith('.{}'.format(v_type))

    @staticmethod
    def win_reduce(file_dir, files_arr, file_path, group_reduce_num=200):
        try:
            urls = []
            groups = []
            for_path = file_path[:file_path.rfind('\\') + 1].strip()
            order = 'copy /b {} {}'

            for ourl in files_arr:
                if ourl.rfind('/') != -1:
                    urls.append(os.path.join(file_dir.strip(), ourl[ourl.rfind('/') + 1:]))
                else:
                    urls.append(os.path.join(file_dir.strip(), ourl))

            rest = len(urls) % group_reduce_num
            times = len(urls) // group_reduce_num

            for i in range(times):
                group_path = for_path + 'group' + str(i) + '.ts'
                os.system(order.format('+'.join(urls[i * group_reduce_num: (i + 1) * group_reduce_num]), group_path))
                groups.append(group_path)

            group_path = for_path + 'group' + str(times) + '.ts'
            os.system(order.format('+'.join(urls[times * group_reduce_num: times * group_reduce_num + rest]), group_path))
            groups.append(group_path)
            print(order.format('+'.join(urls[times * group_reduce_num: times * group_reduce_num + rest]), group_path))
            os.system(order.format('+'.join(groups), file_path.strip()))

            for group in groups:
                os.remove(group)

            return True
        except Exception as e:
            print(repr(e))
            return False

    @staticmethod
    def ffmpeg_reduce(file_dir, files_arr, file_path):
        try:
            files = []
            now_path = os.getcwd()
            temp = 'list.txt'
            order = 'ffmpeg -f concat -i list.txt -c copy {}'

            os.chdir(file_dir)

            if os.path.exists(temp):
                os.remove(temp)

            for ourl in files_arr:
                if ourl.rfind('/') != -1:
                    files.append(ourl[ourl.rfind('/') + 1:])
                else:
                    files.append(ourl)

            with open(temp, 'a', encoding='utf-8') as fp:
                for file in files:
                    fp.write("file \'{}\'\n".format(file))

            os.system(order.format(file_path))
            os.remove(temp)
            os.chdir(now_path)

            return True
        except Exception as e:
            print(repr(e))
            return False
