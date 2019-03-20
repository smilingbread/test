import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BOARD)

btn1, btn2, btn3 = 12, 16, 18

GPIO.setup([btn1, btn2, btn3], GPIO.IN, pull_up_down=GPIO.PUD_UP)
#prevInput1, prevInput2, prevInput3 = 1, 1, 1

#GPIO.wait_for_edge(btn1, GPIO.FALING)
#os.system("sudo reboot")
while True:

    input1, input2, input3 = GPIO.input(
        btn1), GPIO.input(btn2), GPIO.input(btn3)

    
    if(not input1) and (not input2):
        os.system("sudo poweroff")

    if(not input1) and (not input3):
        os.system("sudo reboot")

    #prevInput1, prevInput2, prevInput3 = input1,input2,input3
    time.sleep(0.05)
GPIO.cleanup()