import numpy as np
import matplotlib.pyplot as plt

# Waypoints de la trayectoria deseada
path = np.array([[0.0, 0.0], [2.0, 4.0], [6.0, 5.0], [8.0, 10.0]])

# Parámetros del algoritmo
lookahead = 0.5         # Distancia de anticipación [m]
Kd = 1.3                # Ganancia proporcional de rumbo
v = 0.5                 # Velocidad lineal constante [m/s]
L = 2.0                 # Distancia entre ejes [m]
dt = 0.1                # Paso de tiempo [s]
iteraciones = 285

# Pose inicial del robot (x, y, theta)
x, y, theta = 0.0, 0.0, 0.0
current_index = 0

X, Y = [x], [y]

def angle_wrap(a):
    """Normaliza el ángulo al intervalo [-pi, pi)"""
    return (a + np.pi) % (2.0 * np.pi) - np.pi

# Bucle de control y simulación
for _ in range(iteraciones):
    # 1. Distancia al punto de referencia actual
    dx = path[current_index][0] - x
    dy = path[current_index][1] - y
    dist = np.hypot(dx, dy)
    
    # 2. Conmutar al siguiente waypoint si se entra en la zona de lookahead
    if dist < lookahead and current_index < len(path) - 1:
        current_index += 1
        
    target = path[current_index]
    
    # 3. Dirección hacia el punto objetivo
    dx_target = target[0] - x
    dy_target = target[1] - y
    theta_goal = np.arctan2(dy_target, dx_target)
    
    # 4. Error de rumbo y ley de control de giro
    error = angle_wrap(theta_goal - theta)
    delta = Kd * error
    
    # 5. Integración numérica del modelo cinemático de bicicleta
    x += v * np.cos(theta) * dt
    y += v * np.sin(theta) * dt
    theta += (v / L) * np.tan(delta) * dt
    
    X.append(x)
    Y.append(y)

# Graficación
plt.figure(figsize=(8, 8))
plt.plot(path[:, 0], path[:, 1], 'ro--', linewidth=2, label="Trayectoria deseada (Waypoints)")
plt.plot(X, Y, 'b-', linewidth=2, label="Trayectoria real del robot")
plt.scatter(path[:, 0], path[:, 1], color='red', s=80, zorder=5)
plt.title("Parte 4: Seguimiento de Trayectoria (Pure Pursuit)")
plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.show()