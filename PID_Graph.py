# Importar librerías necesarias
import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
file_path = r'C:\Users\USUARIO\Desktop\Lockdown_project\pid_data.csv'  # Asegúrate de que el archivo esté en la misma carpeta o proporciona la ruta completa
data = pd.read_csv(file_path)

# Mostrar las primeras filas para verificar los datos
print(data.head())

# Graficar los datos
plt.figure(figsize=(10, 6))
plt.plot(data['Tiempo (s)'], data['Setpoint'], label='Setpoint', color='blue', linestyle='--')
plt.plot(data['Tiempo (s)'], data['Salida PID'], label='Salida PID', color='red')

# Añadir etiquetas y título
plt.title('Comportamiento del PID')
plt.xlabel('Tiempo (s)')
plt.ylabel('Grados de inclinacio')
plt.ylim(99.00, 100.90)
plt.legend()

# Mostrar la gráfica
plt.show()
