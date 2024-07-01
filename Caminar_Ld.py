from pca import PCA9685
from machine import I2C, Pin
from servo import Servos
from time import sleep
sda = Pin(0)
scl = Pin(1)
id = 0
i2c = I2C(id=id, sda=sda, scl=scl)
pca = PCA9685(i2c=i2c)
servo = Servos(i2c=i2c)
servo.position(index=0, degrees=85) #+30
servo.position(index=1, degrees=90) #+30
servo.position(index=2, degrees=80) #-20
servo.position(index=3, degrees=90) #-20
sleep(0.3)
while True:
    servo.position(index=0, degrees=115) #paso derecha
    servo.position(index=1, degrees=90)
    servo.position(index=2, degrees=60)
    servo.position(index=3, degrees=90)
    sleep(0.1)
    servo.position(index=0, degrees=85) #paso izquierda
    servo.position(index=1, degrees=60)
    servo.position(index=2, degrees=80)
    servo.position(index=3, degrees=110)
    sleep(0.1)
    servo.position(index=0, degrees=115)
    servo.position(index=1, degrees=90)
    servo.position(index=2, degrees=60)
    servo.position(index=3, degrees=90)
    sleep(0.1)
    