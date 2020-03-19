class ByteTransfer(object):
    relative_arr = ['bit', 'Byte', 'KB', 'MB', 'GB', 'TB']
    total_arr = [0]

    def __init__(self):
        pass

    @staticmethod
    def str_join(str1, str2, join=' '):
        return "%s%s%s" % (str1, join, str2)

    @staticmethod
    def num(byte_num):
        if type(byte_num) == int:
            return byte_num
        else:
            return int(byte_num)

    def byte_to_bit(self, byte_num):
        return self.num(byte_num) * 8

    def byte_s(self, byte_num, r_a_num=1, join=' '):
        num = self.num(byte_num)
        res = num // 1024
        mod = num % 1024

        if res >= 1024:
            p_r_res = self.byte_s(res, r_a_num + 1)
        else:
            p_r_res = str(res) + self.relative_arr[r_a_num + 1]

        if mod != 0:
            return self.str_join(p_r_res, str(mod) + self.relative_arr[r_a_num], join)

    def byte_transfer_about(self, byte_num, r_a_num=1):
        num = self.num(byte_num)
        res = num // 1024
        mod = num % 1024
        self.total_arr.append(mod)
        if res >= 1024:
            return self.byte_transfer_about(res, r_a_num + 1)
        else:
            self.total_arr.append(res)
            r_a_num += 1
            return "%d.%d%s/s" % (self.total_arr[r_a_num], self.total_arr[r_a_num - 1], self.relative_arr[r_a_num])

    def byte_speed(self, byte_num, time_stamp):
        byte_num = self.num(byte_num)
        time_stamp = self.num(time_stamp)
        speed = byte_num // time_stamp
        return self.byte_transfer_about(speed)


if __name__ == "__main__":
    # bt = ByteTransfer()
    # print(bt.byte_s(371112))
    # print(bt.byte_speed(371112, 2.081942558288574))
    pass
