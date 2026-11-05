from roboticstoolbox import Bicycle
import numpy as np
import matplotlib.pyplot as plt

# Aumento drástico del ruido: 0.5 m en distancia y 2.0 grados en orientación
V = np.diag([0.5, np.deg2rad(2.0)])**2
robot = Bicycle(covar=V)
robot_ideal = Bicycle(covar=np.zeros((2,2)))

x_real, y_real, x_ideal, y_ideal = [], [], [], []

# Nueva pose inicial: x=2, y=2, orientación=45 grados
qp_real = [2.0, 2.0, np.pi/4]
qp_ideal = [2.0, 2.0, np.pi/4]

for _ in range(200):
    odo_real = robot.step((1.0, 0.2))
    qp_real = robot.f(qp_real, odo_real)
    
    odo_ideal = robot_ideal.step((1.0, 0.2))
    qp_ideal = robot.f(qp_ideal, odo_ideal)
    
    x_real.append(qp_real[0])
    y_real.append(qp_real[1])
    x_ideal.append(qp_ideal[0])
    y_ideal.append(qp_ideal[1])

plt.figure(figsize=(8,6))
plt.plot(x_ideal, y_ideal, label='Odometría ideal (sin ruido)', linewidth=1)
plt.plot(x_real, y_real, label='Odometría con ruido extremo', linewidth=1)
plt.xlabel('X [m]')
plt.ylabel('Y [m]')
plt.title('Variación 1: Ruido extremo y diferente pose inicial')
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.show()