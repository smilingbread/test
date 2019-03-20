import os
import time

import parameter

# python3.6后dict遍历的顺序与加入顺序一致 故可以不用sort排序


PATH =  parameter.BIN_FILE_PATH

PROD_CLS_CODE = "品种编号"
PROD_CODE = "商品编码"
QTY_IN_TRAN = "在途库存"
QTY_ACBL = "可配库存"
COLOR_ID = "颜色编号"
SPEC_ID = "规格编号"

dict = {}
textProTotal = {}
textPro = {}


def dict_print(map):
    for m in map:
        print(str(m) + ":" + str(map[m]))

# 读取文件


def read_txt(path):

    with open(path, 'r', encoding='gb2312') as f:
        colIndex = {}
        lines = [line.strip().split("\t") for line in f.readlines()]

    for i in range(len(lines[0])):
        colIndex[lines[0][i]] = i

    dict.clear()
    # 各个列名索引
    prodCodeCol = colIndex[PROD_CODE]
    qtyInTranCol = colIndex[QTY_IN_TRAN]
    qtyAcblCol = colIndex[QTY_ACBL]
    colorIdCol = colIndex[COLOR_ID]
    specIdCol = colIndex[SPEC_ID]

    for line in lines[1:]:
        prodCode = line[prodCodeCol]
        qtyInTran = line[qtyInTranCol]
        qtyAcbl = line[qtyAcblCol]
        colorId = line[colorIdCol]
        specId = line[specIdCol]
        prodClsCode = prodCode[:-6]

        if prodClsCode not in dict:
            dict[prodClsCode] = {}

        if colorId not in dict[prodClsCode]:
            dict[prodClsCode][colorId] = {}

        if specId not in dict[prodClsCode][colorId]:
            dict[prodClsCode][colorId][specId] = {}

        dict[prodClsCode][colorId][specId][QTY_ACBL] = int(float(qtyAcbl))
        dict[prodClsCode][colorId][specId][QTY_IN_TRAN] = int(float(qtyInTran))

    """ dict[prodCode] = {
        QTY_IN_TRAN:int(float(line[qtyInTranCol])),
        QTY_ACBL:int(float(line[qtyAcblCol])),
        COLOR_ID:line[colorIdCol],
        SPEC_ID:line[specIdCol],
        } """

# 总计文本字典


def get_total_text():

    textProTotal.clear()
    for proCls in dict:

        string = ""
        for color in sorted(dict[proCls].keys()):
            qtyAcblTotal = 0
            qtyInTranTotal = 0
            for spec in dict[proCls][color]:
                qtyAcblTotal += dict[proCls][color][spec][QTY_ACBL]
                qtyInTranTotal += dict[proCls][color][spec][QTY_IN_TRAN]
            string += color + "=" + \
                str(qtyAcblTotal) + ("+" + str(qtyInTranTotal)
                                     if qtyInTranTotal else "") + ","
        textProTotal[proCls] = string[:-1]

# 文本字典


def get_pro_text():

    textPro.clear()

    for proCls in dict:
        textPro[proCls] = {}
        for color in dict[proCls]:
            string = ""
            for spec in sorted(dict[proCls][color].keys(), key=lambda x: int(x)):
                qtyAcbl = dict[proCls][color][spec][QTY_ACBL]
                qtyInTran = dict[proCls][color][spec][QTY_IN_TRAN]
                string += spec + "=" + \
                    str(qtyAcbl) + ("+" + str(qtyInTran)
                                    if qtyInTran else "") + ","
            textPro[proCls][color] = string[:-1]

# init


def init():
    read_txt(PATH)
    get_total_text()
    get_pro_text()


def main():
    read_txt(PATH)
    get_pro_text()
    print(os.stat(PATH).st_mtime)
    print(time.strftime('%Y-%m-%d %H:%M:%S',
                        time.localtime(os.stat(PATH).st_mtime)))
   # dictPrint(textPro)


if __name__ == "__main__":
    main()
