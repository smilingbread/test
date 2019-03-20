import os
import time

import parameter
import utils

PATH = parameter.RECEIPT_FILE_PATH
PROD_CLS_CODE = "商品品种编号"
PROD_CODE = "商品编号"
COLOR_ID = "颜色编号"
SPEC_ID = "规格编号"
TRADING = "交易时间"
SALES_MAN = "导购员姓名"
SALE_AMOUNT = "销售数量"
START_TIME = ""
END_TIME = ""

_file_mtime = 0
_dict = {}

# 获取数据,并且记录文件修改时间


def get_data(path):
    _dict.clear()
    data = utils.read_txt(path)
    _set_file_mtime()
    title = data[0]

    prod_code_col = title.index(PROD_CODE)
    prod_cls_code_col = title.index(PROD_CLS_CODE)
    trading_col = title.index(TRADING)
    sales_man_col = title.index(SALES_MAN)
    sale_amount_col = title.index(SALE_AMOUNT)

    data = data[1:]
    trading_list = [line[trading_col] for line in data]
    global START_TIME
    global END_TIME
    START_TIME = min(trading_list)[:-2]
    END_TIME = max(trading_list)[:-2]
    data.sort(key=lambda x: x[trading_col])  # 按时间排序
    for record in data[1:]:
        prod_code = record[prod_code_col]
        prod_cls_code = record[prod_cls_code_col]
        trading = record[trading_col][:-2]
        salesman = record[sales_man_col]
        color_id = prod_code[-6:][:4]
        spec_id = int(prod_code[-2:])
        sale_amount = int(float(record[sale_amount_col]))

        if prod_cls_code not in _dict:
            _dict[prod_cls_code] = {}

        if color_id not in _dict[prod_cls_code]:
            _dict[prod_cls_code][color_id] = {}

        # if spec_id in dict[prod_cls_code][color_id]:
        if sale_amount > 0:
            _dict[prod_cls_code][color_id][int(
                spec_id)] = salesman + " #" + trading[2:-3]

# 设置文件修改时间


def _set_file_mtime():
    global _file_mtime
    _file_mtime = os.stat(PATH).st_mtime


# 获取文件更改时间


def get_file_mtime():
    return _file_mtime


# 获取文本


def response(prod_code):
    if prod_code not in _dict:
        return "品种:" + prod_code + "\n" \
               + "从 #" + START_TIME[:10] + "\n" \
               + "至 #" + END_TIME[:10] + "\n" \
               + "无销售记录"
    ret = ""
    prod = _dict[prod_code]
    for color in sorted(prod.keys()):
        ret += "[" + color + "]" + "\n"
        for spec in sorted(prod[color].keys()):
            ret += str(spec) + ":" + prod[color][spec] + "\n"
        ret += "\n"
    return ret + "@@@ " + utils.format_time(get_file_mtime())


# 初始化
def init():
    get_data(PATH)
    _set_file_mtime()


def dict_print(map):
    for m in map:
        print(str(m) + ":" + str(map[m]))


if __name__ == "__main__":
    init()
    while True:
        prod_code = input("输入编号:")
        print(response(prod_code))
