import time

#读取文件转为二维数组 + 列名
def read_txt(path):
    with open(path, 'r', encoding='gb2312') as f:
        lines = [line.strip().split("\t") for line in f.readlines()]
    return lines

# 获取文件更改时间
def format_time(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))