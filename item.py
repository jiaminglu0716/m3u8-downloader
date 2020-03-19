from log import LogWriter
from log import LogSearch
from os.path import exists


class Item(object):
    __dataSet = {}

    def __init__(self, **kwargs):
        pass

    @staticmethod
    def __item_check(val):
        if type(val) != str:
            return str(val)
        else:
            return val

    def add(self, key, val, callback=None):
        self.__dataSet[self.__item_check(key)] = self.__item_check(val)
        if callback:
            callback(key, val)

    @staticmethod
    def show_add(key, val, s_format="{} -> {}"):
        print(s_format.format(key, val))

    def get(self):
        return self.__dataSet

    def clear(self):
        self.__dataSet = {}

    def get_item(self, key):
        return self.__dataSet.get(key)

    # def get_db(self):
    #     return self.linked_db

    def get_arr(self):
        data_arr = []
        for (k, y) in self.__dataSet.items():
            data_arr.append(y)
        return data_arr

    def show(self):
        print(self.__dataSet)

    def show_arr(self):
        print(self.get_arr())

    # def check_db(self, table_name, c_dict):
    #     self.linked_db.use_table(table_name)
    #     vals = self.linked_db.find(c_dict)
    #     return len(vals) != 0

    @staticmethod
    def check(name, *args):
        file = "%s.log" % name
        if exists(file):
            ls = LogSearch(file)
            res = ls.find_all(*args)
            return len(res) != 0
        else:
            with open(file, 'w') as fp:
                fp.close()
            return False

    def save_log(self, name, callback=None):
        lw = LogWriter("%s.log" % name)
        data = self.get_arr()
        lw.write_one(data)
        if callback:
            callback(self.get())

    # def save_db(self, table_name, show=True):
    #     if show:
    #         print(self.get())
    #
    #     self.linked_db.use_table(table_name)
    #     self.linked_db.insert(data=self.get())
    #
    #     self.clear()


if __name__ == '__main__':
    pass
