#Importacion de librerias.
from machine import Pin, UART, I2C, SPI
import random
import gc9a01
import utime
from mpu6050 import init_mpu6050, get_mpu6050_data
from pca import PCA9685
from servo import Servos

# Variables del PID
Kp = 1.0  # Ganancia proporcional
Ki = 0.0  # Ganancia integral
Kd = 0.05  # Ganancia derivativa

previous_error = 0.0
integral = 0.0

def pid_controller(setpoint, measured_value):
    global previous_error, integral

    # Calcular error
    error = setpoint - measured_value

    # Calcular control proporcional
    proportional = Kp * error

    # Calcular control integral
    integral += error
    integral_control = Ki * integral

    # Calcular control derivativo
    derivative = error - previous_error
    derivative_control = Kd * derivative

    # Actualizar error previo
    previous_error = error

    # Salida del PID
    return proportional + integral_control + derivative_control

# Función para mapear valores de un rango a otro
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Configuración del setpoint (posición vertical del torso)
setpoint_z = 99.89  # La posición deseada en el eje z (puedes ajustar esto según tu configuración)

#Inicializacion de driver servos.
sda = Pin(2)
scl = Pin(3)
id = 1
i2c = I2C(id=id, sda=sda, scl=scl)
pca = PCA9685(i2c=i2c)
servo = Servos(i2c=i2c)
spi = SPI(0, baudrate=31250000, sck=Pin(18), mosi=Pin(19))
tft = gc9a01.GC9A01(
spi,
240,
240,
reset=Pin(20, Pin.OUT),
cs=Pin(22, Pin.OUT),
dc=Pin(21, Pin.OUT),
backlight=Pin(26, Pin.OUT),
rotation=0)

tft.init()

for image in ["lock.jpg"]:
    tft.jpg(image, 0, 0, gc9a01.SLOW)
    


#Posicion firme del robot
servo.position(index=0, degrees=85) 
servo.position(index=1, degrees=95) 
servo.position(index=2, degrees=73) 
servo.position(index=3, degrees=90) 
servo.position(index=4, degrees=80)
servo.position(index=5, degrees=100)
servo.position(index=6, degrees=0)
servo.position(index=7, degrees=170)
utime.sleep_ms(100)

#Configurar el LED integrado
led = Pin(25, Pin.OUT)

# Configurar I2C para el MPU6050
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
init_mpu6050(i2c)

# Configurar la UART para comunicarse con el módulo HM-10
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))


while True:
    # Leer el valor del acelerómetro en el eje z
    data = get_mpu6050_data(i2c)
    data += 100
    z_value = data
    print("Acceleration Z: {:.2f} g".format(data))
    
    # Calcular la salida del PID
    pid_output = pid_controller(setpoint_z, z_value)
    
    # Mapear el valor del eje z a los ángulos de los servos
    angle_servo_4 = map_value(pid_output, -1, 1, 84, 76)
    angle_servo_5 = map_value(pid_output, -1, 1, 96, 104)  

    # Aplicar los ángulos a los servos
    servo.position(index=4, degrees=angle_servo_4)
    servo.position(index=5, degrees=angle_servo_5)
    
    print("Servo 4 Angle: {:.2f}".format(angle_servo_4))
    print("Servo 5 Angle: {:.2f}".format(angle_servo_5))
    
    # Verificar si hay datos disponibles en UART
    if uart.any():
        command = uart.read(1)  # Leer un byte de la UART
        if command == b'1':
            servo.position(index=0, degrees=115) #paso derecha
            servo.position(index=1, degrees=90)
            servo.position(index=2, degrees=60)
            servo.position(index=3, degrees=90)
            utime.sleep_ms(300)
            servo.position(index=0, degrees=85) #paso izquierda
            servo.position(index=1, degrees=60)
            servo.position(index=2, degrees=80)
            servo.position(index=3, degrees=110)
            utime.sleep_ms(300)
        elif command == b'0':
            servo.position(index=0, degrees=85) 
            servo.position(index=1, degrees=95) 
            servo.position(index=2, degrees=73) 
            servo.position(index=3, degrees=90) 
            servo.position(index=4, degrees=80)
            servo.position(index=5, degrees=100)
            servo.position(index=6, degrees=0)
            servo.position(index=7, degrees=170)
            

    # Controlar los servomotores 4 y 5 basado en el valor del eje y del acelerómetro
    '''
    if data == 99.67: #posicion derecha
        servo.position(index=4, degrees=52) 
        servo.position(index=5, degrees=128) 
        
    elif data > 99.70: #adelante
        servo.position(index=4, degrees=51) 
        servo.position(index=5, degrees=129)
        
    elif data < 99.65: #atras
        servo.position(index=4, degrees=53)
        servo.position(index=5, degrees=127)

        
    '''
    # Pausa para evitar sobrecargar la CPU
    utime.sleep_ms(50)
