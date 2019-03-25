# 蜂鸣器

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ioPin, vccPin = 36, 38

BEGIN_SECONDS = 2
INTERVALS = {0:0.2,1:1}
SPACE_SCECONDS = 1

GPIO.setup(vccPin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(ioPin, GPIO.OUT, initial=GPIO.HIGH)

#单次
def beep(seconds=1):
    GPIO.output(ioPin, GPIO.LOW)
    time.sleep(seconds)
    GPIO.output(ioPin, GPIO.HIGH)

#输入多次
def beep_action(times, sleepsecs=0.5):
    for i in range(times):
        beep()
        time.sleep(sleepsecs)

def close():
    GPIO.cleanup()

#时转二进制
def to_binlist(h):
    h = h%12 if h > 12 else h
    g= bin(h)[2:].zfill(4)
    ret = [int(x) for x in g]
    return ret

if __name__ == "__main__":
    while True:
        time.sleep(0.05)
        t = time.localtime()
        h = t.tm_hour
        m = t.tm_min
        s = t.tm_sec
        if m == 0 and s == 0:
            temp = to_binlist(h)
            beep(BEGIN_SECONDS)
            time.sleep(SPACE_SCECONDS)
            for ele in temp:
                beep(INTERVALS[ele])
                time.sleep(SPACE_SCECONDS)

    close()



