from pca import PCA9685
from imu import MPU6050
from servo import Servos
import utime
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)
led_1 = Pin(25,Pin.OUT)
pca = PCA9685(i2c=i2c)
servo = Servos(i2c=i2c)

while True:
   led_1.value(1)
   ay = round(imu.accel.y,2)
   print(ay)
   utime.sleep_ms(200)
   if ay < 0:
       servo.position(index=0, degrees=180)
       servo.position(index=1, degrees=180)
       servo.position(index=2, degrees=180)
   elif ay > 0:
       servo.position(index=0, degrees=0)
       servo.position(index=1, degrees=0)
       servo.position(index=2, degrees=0)