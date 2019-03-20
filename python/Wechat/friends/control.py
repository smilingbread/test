import time
import re
import os

import utils
import read_data
import parameter
import receipts

INIT_TEXT = "20180618"

_asks = {}
_last_searchs = {}
_dict6 = {}
file_file_mtime = 0


# 尾数6位对应编号


def _get_dcit6():
    _dict6.clear()
    dict = read_data.dict
    for ele in dict:
        tail = ele[-6:]
        if tail not in _dict6:
            _dict6[tail] = [ele]
        else:
            _dict6[tail].append(ele)

# 完整品种编号回应文本


def response(prodCode):
    str = ""
    str += "品种:" + prodCode + "\n"
    str += "总计:" + read_data.textProTotal[prodCode] + "\n"
    colors = read_data.textPro[prodCode]
    for clo in sorted(colors.keys()):
        str += "[" + clo + "]" + " " + colors[clo] + "\n"

    str += "\n@@@ " + utils.format_time(get_text_mtime())
    return str


# 正则判断
def match(text):
    pattern = r"^\d+$"
    return True if re.match(pattern, text) else False


# asks返回文本


def cmd_asks(fromUser):
    ret = ""
    for number in sorted(_asks[fromUser].keys(), key=lambda x: int(x)):
        ret += number + ": " + _asks[fromUser][number] + "\n"
    return ret

# 设置lastsearch


def update_last_search(from_user, prod_cls_code):
    _last_searchs[from_user] = prod_cls_code

# 在dict6中的处理过程


def do_in_dict6(text, from_user):
    if text not in _dict6:
        return
    if from_user in _asks:
        _asks[from_user].clear()
    prod_cls_code = _dict6[text]
    if len(prod_cls_code) == 1:
        update_last_search(from_user, prod_cls_code[0])
        return response(prod_cls_code[0])
    else:
        _asks[from_user] = {str(x+1): prod_cls_code[x]
                            for x in range(len(prod_cls_code))}
        return cmd_asks(from_user)

# 在asks中的处理过程,必须确保存在


def do_in_asks(text, from_user):
    prod_cls_code = _asks[from_user][text]
    update_last_search(from_user, prod_cls_code)
    _asks[from_user].clear()
    if prod_cls_code not in read_data.dict:
        return "数据已更新,请重新输入品种号"
    #ret = response(prod)
    return response(prod_cls_code)

# 设置文件修改日期


def set_text_mtime():
    global file_file_mtime
    file_file_mtime = os.stat(read_data.PATH).st_mtime

# 获取文件更改时间


def get_text_mtime():
    return file_file_mtime

# is_reread_bin判断库存文件修改 如果更改则重新读取时间


def is_reread_bin():
    newFileMtime = os.stat(parameter.BIN_FILE_PATH).st_mtime
    return newFileMtime > file_file_mtime

# is_reread_bin判断小票文件修改 如果更改则重新读取时间


def is_reread_receipt():
    newFileMtime = os.stat(parameter.RECEIPT_FILE_PATH).st_mtime
    return newFileMtime > receipts.get_file_mtime()


# 初始化库存数据


def _reread_bin():
    #start = time.time()

    set_text_mtime()
    read_data.init()

    #end = time.time()
    # return "It run time is : %.3f seconds" % (end-start)
    # print(response("15088511044"))
    # read_data.dictPrint(dict6)


# 初始化小票数据
def _reread_receipts():
    receipts.init()

# 初始化


def init():
    _reread_bin()
    _get_dcit6()
    _reread_receipts()

# 获取小票信息


def _get_receipt( from_user):
    if from_user in _last_searchs:
        return receipts.response(_last_searchs[from_user])


# TextCmd
def analysis(text, from_user):

    if is_reread_bin():
        _reread_bin()

    if is_reread_receipt():
        _reread_receipts()

    if not match(text):
        return

    if len(text) == 6 and text not in _dict6:
        return "查无结果"

    if text == "000":
        return _get_receipt(from_user)

    if from_user in _asks and text in _asks[from_user]:
        return do_in_asks(text, from_user)
    else:
        ret = do_in_dict6(text, from_user)
        return ret

    # update_last_search(prod_cls_code,from_user)


""" if fromUser not in _asks:
        if text in _dict6:
            update_last_search(text,format)
            return do_in_dict6(text, fromUser)
    else:
        if text in _asks[fromUser]:
            prod_cls_code = do_in_asks(text,fromUser)
            update_last_search(prod_cls_code,fromUser)
            return do_in_asks(text, fromUser)
        else:
            if text in _dict6:
                update_last_search(text,format)
                return do_in_dict6(text, fromUser) """


if __name__ == "__main__":
    init()
    from_user = "pg"
    while True:
        text = input("请输入数字:").strip()
        print(analysis(text, "pg"))
