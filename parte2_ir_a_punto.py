import numpy as np
import matplotlib.pyplot as plt

# Condición inicial del robot (x, y, theta)
x, y, theta = 0.0, 0.0, 0.0

# Posición objetivo
goal = np.array([5.0, 5.0])

# Ganancias del controlador
Kv = 0.5        # Ganancia proporcional de velocidad
Kh = 1.5        # Ganancia proporcional de orientación (steering)

# Parámetros del modelo
L = 2.0         # Distancia entre ejes [m]
dt = 0.1        # Paso de tiempo [s]

# Inicialización
distance = np.hypot(goal[0] - x, goal[1] - y)
X, Y = [x], [y]

def wrap_angle(angle):
    """Normaliza el ángulo al intervalo [-pi, pi)"""
    return (angle + np.pi) % (2.0 * np.pi) - np.pi

# Bucle de control hasta estar a menos de 10 cm del objetivo
while distance > 0.1:
    dx = goal[0] - x
    dy = goal[1] - y
    distance = np.hypot(dx, dy)
    
    # Rumbo objetivo hacia la meta
    theta_goal = np.arctan2(dy, dx)
    
    # Error angular normalizado
    heading_error = wrap_angle(theta_goal - theta)
    
    # Leyes de control
    v = Kv * distance
    delta = Kh * heading_error
    
    # Integración del modelo cinemático tipo bicicleta
    x += v * np.cos(theta) * dt
    y += v * np.sin(theta) * dt
    theta += (v / L) * np.tan(delta) * dt
    
    X.append(x)
    Y.append(y)

# Graficación
plt.figure(figsize=(7, 7))
plt.plot(X, Y, 'b-', linewidth=2, label="Trayectoria del robot")
plt.scatter(goal[0], goal[1], color='red', marker='x', s=120, label=f"Meta {goal}")
plt.scatter(X[0], Y[0], color='green', marker='o', s=80, label="Inicio (0,0)")
plt.title("Parte 2: Control - Ir a un Punto")
plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.show()