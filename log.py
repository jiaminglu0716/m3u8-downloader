import time
from calTime import timestamp_to_date


class LogReader(object):
    def __init__(self, f_name):
        self.i_stream = open(f_name, 'r')

    @staticmethod
    def __out(line):
        content = line[line.find('#') + 1:-1]
        return content.split('?')

    def read_one(self, line=1):
        if line > 1:
            for i in range(1, line):
                self.i_stream.readline()
        return self.__out(self.i_stream.readline())

    def read_all(self):
        res = []
        for line in self.i_stream.readlines():
            res.append(self.__out(line))
        return res

    def count(self):
        return len(self.read_all())

    def close(self):
        self.i_stream.close()


class LogWriter(object):
    def __init__(self, f_name, f_new=False):
        self.o_stream = open(f_name, 'w' if f_new else 'a')

    @staticmethod
    def __get(arr):
        return "{}#{}\n".format(timestamp_to_date(time.time()), '?'.join(arr))

    def write_all(self, arr):
        for i in arr:
            self.write_one(i)

    def write_one(self, arr):
        self.o_stream.write(self.__get(arr))

    def close(self):
        self.o_stream.close()


class LogSearch(LogReader, LogWriter):
    def __init__(self, f_name):
        super().__init__(f_name)
        self.io_stream = open(f_name, 'r+')

    def find_one(self, *args):
        res = self.find_all(*args)
        if res:
            return res[0]
        else:
            return None

    def find_all(self, *args):
        arr = []
        for item in self.read_all():
            res = True
            for arg in args:
                if arg not in item:
                    res = False
                    break
            if res:
                arr.append(item)
        return arr

    def delete_one(self, *args):
        # con = self.find_one(*args)
        pass

    def delete_all(self):
        pass

    def update_one(self):
        pass

    def update_all(self):
        pass

    def drop_log(self):
        pass

    def close(self):
        self.o_stream.close()
        self.i_stream.close()
        self.io_stream.close()


if __name__ == '__main__':
    # lw = LogWriter('m3u8.log')
    # lw.write_all([
    #     ['ming', str(13)],
    #     ['ling', str(15)]
    # ])
    # lw.close()

    # lr = LogReader('m3u8.log')
    # print(lr.read_one(1))

    # ls = LogSearch('m3u8.log')
    # ls.find_all(['ming', '13'])
    pass

