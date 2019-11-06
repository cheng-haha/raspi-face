
import RPi.GPIO as GPIO
import time

P_SERVO = 24 # GPIO端口号，根据实际修改
fPWM = 50  # Hz (软件PWM方式，频率不能设置过高)
a = 10
b = 2

def setup():
    global pwm
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(P_SERVO, GPIO.OUT)
    pwm = GPIO.PWM(P_SERVO, fPWM)
    pwm.start(0)

def setDirection(direction):
    duty = a / 180 * direction + b
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.05)
def sg():
    setup()
    try:
        for i in range(1):
            for direction in range(0, 91, 10):
                setDirection(direction)
            direction = 0
            time.sleep(3)
            setDirection(0)
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()




