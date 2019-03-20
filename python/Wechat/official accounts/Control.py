import ReadData
import time
import re
import os

INIT_TEXT = "20180618"

asks = {}
dict6 = {}
fileFileMtime = 0


# 尾数6位对应编号


def getDcit6():
    dict6.clear()
    dict = ReadData.dict
    for ele in dict:
        tail = ele[-6:]
        if tail not in dict6:
            dict6[tail] = [ele]
        else:
            dict6[tail].append(ele)

# 完整品种编号回应文本


def response(prodCode):
    str = ""
    str += "品种:" + prodCode + "\n"
    str += "总计:" + ReadData.textProTotal[prodCode] + "\n"
    colors = ReadData.textPro[prodCode]
    for clo in sorted(colors.keys()):
        str += "[" + clo + "]" + " " + colors[clo] + "\n"
    
    str += "\n@@@ " + getTextMtime()
    return str


# 正则判断
def match(text):
    pattern = "^\d+$"
    return True if re.match(pattern, text) else False


# asks返回文本


def cmdAsks(fromUser):
    ret = ""
    for number in sorted(asks[fromUser].keys(),key = lambda x:int(x)):
        ret += number + ": " + asks[fromUser][number] + "\n"
    return ret

# 在dict6中的处理过程


def doInDict6(text, fromUser="pg"):
    if fromUser in asks:
        asks[fromUser].clear()
    prods = dict6[text]
    if len(prods) == 1:
        return response(prods[0])
    else:
        asks[fromUser] = {str(x+1): prods[x] for x in range(len(prods))}
        return cmdAsks(fromUser)

# 在asks中的处理过程


def doInAsks(text, fromUser="pg"):
    prod = asks[fromUser][text]
    asks[fromUser].clear()
    if prod not in ReadData.dict:
        return "数据已更新,请重新输入品种号"
    ret = response(prod)    
    return ret

# 设置文件修改日期


def setTextMtime():
    global fileFileMtime
    fileFileMtime = os.stat(ReadData.PATH).st_mtime


# 获取文件更改时间
def getTextMtime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(fileFileMtime))


#isReread判断修改时间 如果更改则重新读取时间
def isReread():
    newFileMtime = os.stat(ReadData.PATH).st_mtime
    return newFileMtime > fileFileMtime

# 初始化


def init():
    start = time.time()

    setTextMtime()
    ReadData.init()
    getDcit6()

    end = time.time()
    return "It run time is : %.03f seconds" % (end-start)
    # print(response("15088511044"))
    # ReadData.dictPrint(dict6)


# TextCmd
def analysis(text, fromUser):

    if isReread():
        init()

    if not match(text):
        return

    if len(text) == 6 and text not in dict6:
        return "无此品种"

    if text == INIT_TEXT:
        return init()

    if fromUser not in asks:
        if text in dict6:
            return doInDict6(text, fromUser)
    else:
        if text in asks[fromUser]:
            return doInAsks(text, fromUser)
        else:
            if text in dict6:
                return doInDict6(text, fromUser)


if __name__ == "__main__":
    init()
    fromUser = "pg"
    while True:
        text = input("请输入数字:")

        if not match(text):
            continue    

        if fromUser not in asks:
            if text in dict6:
                print(doInDict6(text))
        else:
            if text in asks[fromUser]:
                print(doInAsks(text, fromUser="pg"))
                # print(response(asks[fromUser][text]))
                # asks[fromUser].clear()
            else:
                if text in dict6:
                    print(doInDict6(text))
