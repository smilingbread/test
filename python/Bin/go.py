#!/usr/bin/env python3

# v8-结果按价格降序排列

import csv
import os
import time
import sys

import score

CSV_PATH = 'bin.csv'
English = True
MAX_INT = 99999

dict = {}
dict2 = {}
dict3 = {}
dict4 = {}
dict5 = {}
dict6 = {}
dicts = {2: dict2, 3: dict3, 4: dict4, 5: dict5, 6: dict6}

LENGTHS = [2, 3, 4, 5, 6]

PROMPT = "请输入一个数字:"  # "(数字可以是2-6位,或者完整的品种编号):"
COL1_NAME = "品种编号"
COL2_NAME = "价格"
COL3_NAME = "货位"
SAY_BYE = "再见!"
NOT_FONUD = "无此记录,"
RELOAD = "重新载入..."

if English:
    PROMPT = "input numbers:"
    COL1_NAME = "ProCls"
    COL2_NAME = "Price"
    COL3_NAME = "Bin"
    SAY_BYE = "byebye"
    NOT_FONUD = "404,"
    RELOAD = "reloading..."

#NOT_FONUD = "404"
ROWS_COUNT = 11
SEX_COLOR = {"1": "\33[00m", "0": "\33[41m"}
RED_WHITE = "\033[41;37m"
HEADERCOLOR = "\033[47;34m"
NOCOLOR = "\33[0m"

COL1_LENGTH, COL2_LENGTH, COL3_LENGTH = 15, 10, 11

RELOAD_CMD = "000000"
QUIT_CMD = ".88"

GOODS_BIN_KEY = "goodsBin"
PRICE_KEY = "price"

# 从csv文本读入


def read_csv(csvPath):
    # 读取csv信息到dict
    with open(csvPath) as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            proCls = row[0]
            price = row[1]
            goodsBin = row[-1]
            if not proCls.isnumeric():
                continue
            if proCls not in dict:
                #dict[proCls] = {GOODS_BIN_KEY: goodsBin}
                dict[proCls] = {GOODS_BIN_KEY: [goodsBin], PRICE_KEY: price}
            else:
                # dict[proCls][GOODS_BIN_KEY] = dict[proCls][GOODS_BIN_KEY] + \
                #    "," + goodsBin
                temp = dict[proCls][GOODS_BIN_KEY]
                if goodsBin not in temp:
                    temp.append(goodsBin)
    return

# 创建右边位数的索引


def create_index(procls, length):
    dicts[length].clear()
    for ele in procls:
        k = ele[-length:]
        if k not in dicts[length]:
            dicts[length][k] = [ele]
        else:
            dicts[length][k].append(ele)
    return

# 初始化,这个再刚开始运行与输入8个0的时候运行


def init():
    start = time.time()
    dict.clear()
    for d in dicts.values():
        d.clear()
    read_csv(CSV_PATH)
    for length in LENGTHS:
        create_index(dict.keys(), length)
    sort_bin()
    del_invaild_bin()
    end = time.time()
    return end-start


# 货位列表转字符串


def to_string(arraylist):
    ret = ""
    for ele in arraylist:
        ret = ret + str(ele)+","
    return ret[:-1]


# dict排序
def sort_bin():
    for key in dict.keys():
        dict[key][GOODS_BIN_KEY].sort(
            key=lambda x: int(x) if x.isnumeric() else MAX_INT)

#


def del_invaild_bin():
    for key in dict.keys():
        del_invaild(dict[key][GOODS_BIN_KEY])

# 删除多余货位


def del_invaild(mylist):
    temp = mylist[0]
    if len(mylist) <= 1:
        return

    for ele in mylist[:]:
        if not ele.isnumeric():
            break
        elif ele.isnumeric() and (int(ele) == int(temp)+10):
            mylist.remove(ele)
        temp = ele

# 解析数字,返回品种编号列表


def analysis(text):
    length = len(text)
    ret = 0
    if length in LENGTHS:
        tempditc = dicts[length]
        if text not in tempditc:
            ret = []
        else:
            ret = tempditc[text]
    else:
        if text not in dict:
            ret = []
        else:
            ret = [text]
    return ret

# display


def show_header():
    len1 = COL1_LENGTH
    len2 = COL2_LENGTH
    len3 = COL3_LENGTH
    if not English:
        len1 = len1 - len(COL1_NAME)
        len3 = len3 - len(COL3_NAME)
        len2 = len2 - len(COL2_NAME)
    print(HEADERCOLOR + COL1_NAME.ljust(len1) + COL2_NAME.ljust(len2)
          + COL3_NAME.ljust(len3) + NOCOLOR)


def show_center(fooList):
    resList = ["" for ele in range(ROWS_COUNT)]
    if len(fooList) > 11:
        fooList = fooList[:11]
    listLen = len(fooList)
    for i in range(listLen):
        resList[i] = resList[i] + fooList[i]
    for ele in resList:
        print(ele)

# 结果转换为列表,列表每个都是字符串,后与showCenter的list相加


def covert_list(keys):
    ret = []
    for key in keys:
        sex = key[7]
        ret.append(SEX_COLOR[sex] +
                   (key[:2] + "-" + key[2:]
                    ).ljust(COL1_LENGTH)  # 品种编号
                   + (dict[key][PRICE_KEY]).ljust(COL2_LENGTH)
                   # 货位
                   + to_string(dict[key][GOODS_BIN_KEY]).ljust(COL3_LENGTH) +
                   NOCOLOR)
    return ret

# 显示


def display(fooList=[]):
    clear = "cls" if os.name == "nt" else "clear"
    os.system(clear)
    show_header()
    show_center(fooList)
    return

# 查询


def reserch(text):
    ret = []
    nos = text.split(".")
    for no in nos:
        ret += analysis(no)
    ret = list(set(ret))  # 去除重复值
    if len(ret) == 0:
        display()
        print(RED_WHITE + NOT_FONUD + NOCOLOR, end="")
    else:
        display(covert_list(sorted(ret, key=strategy)))

# 扣分


def deduct_score(text):
    text = text[1:]
    n = score.writeto_csv(*text.split("."))
    print("Add " + RED_WHITE + str(n)+NOCOLOR + " records...")
    time.sleep(1)
    display()

# 命令


def command(text):

    if text == QUIT_CMD:
        sys.exit(SAY_BYE)
    elif text == RELOAD_CMD:
        using_time = init()
        print("It run time is : %.03f seconds" %using_time)
        time.sleep(1)
        display()
    else:
        if score.match1(text):
            deduct_score(text)
        else:
            reserch(text)
    return


# 结果排序算法,这边是按照价格降序排列
def strategy(x):
    return -int(dict[x][PRICE_KEY])


if __name__ == "__main__":

    using_time = init()

    print("It run time is : %.03f seconds" %using_time)

    time.sleep(1)
    display()
    while True:
        text = input(HEADERCOLOR + PROMPT + NOCOLOR + "   ").replace(" ", "")
        if text=="":
            print("\033[1A\r\033[K",end="")
            continue
        command(text)
