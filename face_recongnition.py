'''
通过摄像头拍一张照片，然后识别出人是谁，进而控制门禁系统
@author: 程东洲
@date:2019年11月2日
'''

from aip import AipFace
from picamera import PiCamera
import urllib.request
#import RPi.GPIO as GPIO
import base64
import time
#import pyttsx3
import pygame
import os
import RPi.GPIO
import time
import atexit


atexit.register(RPi.GPIO.cleanup)


# 按钮输出针脚连接的GPIO口
btnR=18
servopin=4

#百度人脸识别API账号信息
APP_ID = '****'
API_KEY = '用自己的key'
SECRET_KEY ='用自己的key'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)
#图像编码方式
IMAGE_TYPE='BASE64'
#用户组信息
GROUP = 'chengdz'
camera = PiCamera()
#engine = pyttsx3.init()
pygame.mixer.init()
#GPIO_IN_PIN = 15
#GPIO_OUT_PIN1 = 11
#GPIO_OUT_PIN2 = 13
#定义一个摄像头对象
def getimage():
    camera.resolution = (1024,768)
    camera.start_preview()
    time.sleep(2)
    camera.capture('faceimage.jpg')
    pygame.mixer.music.load('./voice/start.mp3')
    pygame.mixer.music.play()
    time.sleep(2)

#对图片的格式进行转换
def transimage():
    f = open('faceimage.jpg','rb')
    img = base64.b64encode(f.read())
    return img
#播放声音
def playvioce(name):
    pygame.mixer.music.load('./voice/' +name)
    pygame.mixer.music.play()
#发送信息到微信上
def sendmsg(name,main):
    url = "https://sc.ftqq.com/ 用自己的sever酱接口"
    urllib.request.urlopen(url + "text="+name+"&desp="+main)

#上传到百度api进行人脸检测
def go_api(image):
    result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP);
    if result['error_msg'] == 'SUCCESS':
        name = result['result']['user_list'][0]['user_id']
        score = result['result']['user_list'][0]['score']
        if score > 80:
            print("Welcome %s !" % name)
            if name == 'cheng':
                sendmsg("DoorOpen",name)
                #playvioce('fanghao.mp3')
                time.sleep(3)
            if name == 'zhong':
                sendmsg("DoorOpen",name)
                time.sleep(3)
        else:
            print("Sorry...I don't know you !")
            playvioce('noroot.mp3')
            name = 'Unknow'
            return 0
        curren_time = time.asctime(time.localtime(time.time()))
        f = open('Log.txt','a')
        f.write("Person: " + name + "     " + "Time:" + str(curren_time)+'\n')
        f.close()
        return 1
    if result['error_msg'] == 'pic not has face':
        print('There is no face in image!')
        playvioce('face.mp3')
        time.sleep(2)
        return 0
    else:
        print(result['error_code']+' ' + result['error_code'])
        return 0





# 舵机旋转的角度
def rotate(p, angle):
    p.ChangeDutyCycle(7.5+10*angle/180)
    time.sleep(1)
    p.ChangeDutyCycle(0)



#主函数
if __name__ == '__main__':
    playvioce('waite.mp3')
    time.sleep(3)
    try:
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        # 按钮连接的GPIO针脚的模式设置为信号输入模式，同时默认拉高GPIO口电平，
        # 当GND没有被接通时，GPIO口处于高电平状态，取的的值为1
        # 注意到这是一个可选项，如果不在程序里面设置，通常的做法是通过一个上拉电阻连接到VCC上使之默认保持高电平
        RPi.GPIO.setup(btnR, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
        RPi.GPIO.setup(servopin, RPi.GPIO.OUT, initial=False)
        p = RPi.GPIO.PWM(servopin, 50)  # 50HZ
        p.start(0)
        time.sleep(2)


        while True:

            if True:
                time.sleep(0.08)
                #RPi.GPIO.output(R, False)
                print('请按按钮开启人脸识别：')
                if (RPi.GPIO.input(btnR) == 0):
                    getimage()
                    img = transimage()
                    res = go_api(img)
                    if(res == 1):
                        rotate(p, 90)
                        time.sleep(3)
                        os.system("mosquitto_pub -h 用自己的云服务器地址 -t /ESP1/GPIO/16 -m -1")
                        print("okkk")
                        rotate(p,0)
                    else:
                        os.system("mosquitto_pub -h 同上 -t /ESP1/GPIO/16 -m -0")
                        print("noooo")
                        time.sleep(1)
                    print('waite 3 seconds to do next')
                    playvioce('waite.mp3')
                    time.sleep(3)
    except KeyboardInterrupt:
        os.system("mosquitto_pub -h 同上 -t /ESP1/GPIO/16 -m -0")
        pass
