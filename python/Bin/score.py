import datetime
import re
import os

TEXT_PATH = os.path.join(os.path.dirname(__file__), "data/.fuck.csv")
PATTERN = "^\+.*$"
PATTERN1 = "^\d{3}--?\d+$"

RED_WHITE = "\033[41;37m"
NOCOLOR = "\33[0m"


def match1(text):
    """
    判断是否前面加上+,如果则是扣钱模式
    """

    return True if re.match(PATTERN, text) else False


def match2(text):
    """
    判断是不是332-5类似这样的模式
    """
    return True if re.match(PATTERN1, text) else False


def get_now_str():
    """
    返回当前时间
    """
    return datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')


def writeto_csv(*record):
    """
    写入文本,返回成功添加的信息
    """
    now = get_now_str()
    ret = 0
    with open(TEXT_PATH, "a") as file:
        for r in record:
            if not match2(r):
                continue
            ret += 1
            tup = r.split("-", 1)
            file.write(tup[0] + "," +
                       tup[1]+"," +
                       now + "\n")
    return ret


if __name__ == "__main__":
    while True:
        text = input("请输入:  ").replace(" ", "")
        if text.lower() == "quit":
            print("退出...")
            break
        n = writeto_csv(*text.split("."))
        if n:
            print("添加 " + RED_WHITE + str(n) + NOCOLOR + " 条记录...")
        else:
            print("输入错误, ", end="")

# print(writeToCsv("332-1","334-10","dasdad"))

# print(getNowStr())
#print(time.strftime('%Y/%m/%d %H:%M:%S',time.localtime()))
# print(datetime.datetime.now())
