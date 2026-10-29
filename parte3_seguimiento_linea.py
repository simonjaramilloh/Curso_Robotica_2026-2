import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la recta: ax + by + c = 0
# Para a=1, b=-2, c=4 -> y = 0.5*x + 2
a, b, c = 1.0, -2.0, 4.0

# Pose inicial del robot: (x, y, theta)
x, y, theta = 8.0, 5.0, np.pi / 2.0

# Ganancias del controlador
Kd = 0.5        # Ganancia sobre el error lateral (distancia)
Kh = 1.0        # Ganancia sobre el error de rumbo (orientación)

# Parámetros del modelo cinemático tipo bicicleta
dt = 0.1
L = 2.0
v = 1.0
iteraciones = 200

X, Y = [], []

def wrap_angle(angle):
    """Normaliza el ángulo al intervalo [-pi, pi)"""
    return (angle + np.pi) % (2.0 * np.pi) - np.pi

# Bucle de simulación
for _ in range(iteraciones):
    # 1. Distancia ortogonal con signo a la recta
    distance = (a * x + b * y + c) / np.sqrt(a**2 + b**2)
    
    # 2. Orientación de la recta
    theta_line = np.arctan2(a, -b)
    
    # 3. Error angular normalizado
    heading_error = wrap_angle(theta_line - theta)
    
    # 4. Ley de control combinada
    delta = Kd * distance + Kh * heading_error
    
    # 5. Integración numérica del modelo cinemático
    x += v * np.cos(theta) * dt
    y += v * np.sin(theta) * dt
    theta += (v / L) * np.tan(delta) * dt
    
    X.append(x)
    Y.append(y)

# Generación de la línea objetivo para graficar
x_line = np.linspace(min(min(X), 0.0), max(max(X), 12.0), 100)
if b != 0:
    y_line = (-a * x_line - c) / b
else:
    x_line = np.full(100, -c / a)
    y_line = np.linspace(-2, 10, 100)

# Graficación
plt.figure(figsize=(8, 6))
plt.plot(X, Y, 'b-', linewidth=2, label="Trayectoria del robot")
plt.plot(x_line, y_line, 'r--', linewidth=2, label=r"Línea objetivo ($x - 2y + 4 = 0$)")
plt.scatter(X[0], Y[0], color='green', marker='o', s=90, label=r"Inicio $(8, 5, \pi/2)$")
plt.title("Parte 3: Seguimiento de Línea")
plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.show()