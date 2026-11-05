from roboticstoolbox import Bicycle
import numpy as np
import matplotlib.pyplot as plt

# Covarianza del ruido: incertidumbre para estimación de pose
V = np.diag([0.2, np.deg2rad(0.5)])**2
print("Matriz de covarianza V:\n", V)

# Robot con ruido
robot = Bicycle(covar=V)

# Robot ideal (sin ruido)
robot_ideal = Bicycle(covar=np.zeros((2,2)))

# Variables para almacenar trayectorias
x_real = []
y_real = []
x_ideal = []
y_ideal = []
qp_real = [0, 0, 0]
qp_ideal = [0, 0, 0]

# Simulación
for _ in range(200):
    # Movimiento robot real
    odo_real = robot.step((1.0, 0.2))
    qp_real = robot.f(qp_real, odo_real)
    
    # Movimiento robot ideal
    odo_ideal = robot_ideal.step((1.0, 0.2))
    qp_ideal = robot.f(qp_ideal, odo_ideal)
    
    # Guardar trayectoria real
    x_real.append(qp_real[0])
    y_real.append(qp_real[1])
    
    # Guardar trayectoria ideal
    x_ideal.append(qp_ideal[0])
    y_ideal.append(qp_ideal[1])

# Graficar trayectorias
plt.figure(figsize=(8,6))
plt.plot(x_ideal, y_ideal, label='Trayectoria estimada con odometría sin ruido', linewidth=1)
plt.plot(x_real, y_real, label='Trayectoria estimada con odometría con ruido', linewidth=1)
plt.xlabel('X [m]')
plt.ylabel('Y [m]')
plt.title('Comparación de trayectorias')
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.show()