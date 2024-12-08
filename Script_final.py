#Importacion de librerias.
from machine import Pin, UART, I2C, SPI
import random
import gc9a01
import utime
from mpu6050 import init_mpu6050, get_mpu6050_data
from pca import PCA9685
from servo import Servos

# Variables del PID
Kp = 1.3  # Ganancia proporcional
Ki = 0.05  # Ganancia integral
Kd = 1.0  # Ganancia derivativa

previous_error = 0.0
integral = 0.0

PID_MIN = -0.10  # Límite mínimo de salida del PID
PID_MAX = 0.10   # Límite máximo de salida del PID
INTEGRAL_LIMIT = 0.10  # Límite para evitar acumulación excesiva del error integral

def pid_controller(setpoint, measured_value):
    global previous_error, integral

    # Calcular error
    error = setpoint - measured_value

    # Calcular control proporcional
    proportional = Kp * error

    # Calcular control integral
    integral += error
    integral = max(min(integral, INTEGRAL_LIMIT), -INTEGRAL_LIMIT)  # Limitar la integral
    integral_control = Ki * integral

    # Calcular control derivativo
    derivative = error - previous_error
    derivative_control = Kd * derivative

    # Actualizar error previo
    previous_error = error

    # Calcular la salida del PID
    pid_output = proportional + integral_control + derivative_control
    
    # Limitar la salida del PID
    return max(min(pid_output, PID_MAX), PID_MIN)
    
    

# Función para mapear valores de un rango a otro
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Configuración del setpoint (posición vertical del torso)
setpoint = 99.865   # La posición deseada en el eje z (puedes ajustar esto según tu configuración)

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
servo.position(index=1, degrees=125) 
servo.position(index=2, degrees=70) 
servo.position(index=3, degrees=82) 
servo.position(index=4, degrees=70)
servo.position(index=5, degrees=110)
servo.position(index=6, degrees=0)
servo.position(index=7, degrees=177)
utime.sleep_ms(500)

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
    measured_value = data
    print("Measured_value: {:.3f} g".format(measured_value))
    
    # Calcular la salida del PID
    pid_output = pid_controller(setpoint, measured_value)
    print("PID: {:.2f} g".format(pid_output))
    
    # Mapear el valor del eje z a los ángulos de los servos
    angle_servo_4 = map_value(pid_output, PID_MAX, PID_MIN, 75, 71)
    angle_servo_5 = map_value(pid_output, PID_MAX, PID_MIN, 105, 109)  

    # Aplicar los ángulos a los servos
    servo.position(index=4, degrees=angle_servo_4)
    servo.position(index=5, degrees=angle_servo_5)
    
    print("Servo 4 Angle: {:.2f}".format(angle_servo_4))
    print("Servo 5 Angle: {:.2f}".format(angle_servo_5))
    
    # Verificar si hay datos disponibles en UART
    if uart.any():
        command = uart.read(1)  # Leer un byte de la UART
        if command == b'1':
            servo.position(index=0, degrees=100) #paso derecha
            servo.position(index=4, degrees=82)
            servo.position(index=5, degrees=98)
            utime.sleep_ms(150)
            servo.position(index=1, degrees=105)
            servo.position(index=4, degrees=82)
            servo.position(index=5, degrees=98)
            utime.sleep_ms(150)
            servo.position(index=0, degrees=85)
            servo.position(index=1, degrees=125)
            servo.position(index=4, degrees=82)
            servo.position(index=5, degrees=98)
        elif command == b'0':
            servo.position(index=0, degrees=85) 
            servo.position(index=1, degrees=125) 
            servo.position(index=2, degrees=70) 
            servo.position(index=3, degrees=82) 
            servo.position(index=4, degrees=72)
            servo.position(index=5, degrees=108)
            servo.position(index=6, degrees=0)
            servo.position(index=7, degrees=177)
        elif command == b'2':
            servo.position(index=6, degrees=90)
            servo.position(index=4, degrees=70)
            servo.position(index=5, degrees=110)
            utime.sleep_ms(500)
            servo.position(index=6, degrees=70)
            servo.position(index=4, degrees=70)
            servo.position(index=5, degrees=110)
            utime.sleep_ms(200)
            servo.position(index=6, degrees=90)
            servo.position(index=4, degrees=70)
            servo.position(index=5, degrees=110)
            utime.sleep_ms(200)
            servo.position(index=6, degrees=70)
            servo.position(index=4, degrees=70)
            servo.position(index=5, degrees=110)
            utime.sleep_ms(200)
            servo.position(index=6, degrees=90)
            servo.position(index=4, degrees=70)
            servo.position(index=5, degrees=110)
            utime.sleep_ms(200)
            servo.position(index=6, degrees=70)
            servo.position(index=4, degrees=70)
            servo.position(index=5, degrees=110)
            utime.sleep_ms(200)
            servo.position(index=6, degrees=0)
            servo.position(index=4, degrees=70)
            servo.position(index=5, degrees=110)
            
        
            
    # Pausa para evitar sobrecargar la CPU
    utime.sleep_ms(100)