import numpy as np
import matplotlib.pyplot as plt

# Parámetros del modelo y controlador
L = 2.0                 # Wheelbase [m]
Kv = 0.5                # Ganancia de velocidad
Kh = 1.5                # Ganancia de dirección
dt = 0.1                # Paso de integración [s]
goal = np.array([5.0, 5.0])

# Límite físico de giro del volante (máximo 35 grados para evitar asíntota de tan)
delta_max = np.radians(35.0)

def wrap_angle(angle):
    """Normaliza el ángulo al intervalo [-pi, pi)"""
    return (angle + np.pi) % (2.0 * np.pi) - np.pi

# 5 Casos de estudio dentro del cuadrante positivo
casos = [
    {"label": r"$\theta_0 = 0^\circ$ (Caso base horizontal)", "theta0": np.radians(0),  "color": "#1f77b4"},
    {"label": r"$\theta_0 = 20^\circ$",                      "theta0": np.radians(20), "color": "#ff7f0e"},
    {"label": r"$\theta_0 = 45^\circ$ (Directo a la meta)",   "theta0": np.radians(45), "color": "#2ca02c"},
    {"label": r"$\theta_0 = 65^\circ$",                      "theta0": np.radians(65), "color": "#9467bd"},
    {"label": r"$\theta_0 = 85^\circ$ (Casi vertical)",      "theta0": np.radians(85), "color": "#d62728"}
]

plt.figure(figsize=(8, 8))

for caso in casos:
    x, y = 0.0, 0.0
    theta = caso["theta0"]
    
    X, Y = [x], [y]
    distance = np.hypot(goal[0] - x, goal[1] - y)
    
    # Bucle de control con umbral de parada en 0.1 m
    while distance > 0.1:
        dx = goal[0] - x
        dy = goal[1] - y
        distance = np.hypot(dx, dy)
        
        # Orientación hacia el objetivo
        theta_goal = np.arctan2(dy, dx)
        error = wrap_angle(theta_goal - theta)
        
        # Leyes de control con saturaciones físicas
        v = min(Kv * distance, 1.5)               # Velocidad lineal acotada
        delta = np.clip(Kh * error, -delta_max, delta_max)  # Giro acotado a +/- 35°
        
        # Integración cinemática (Bicicleta)
        x += v * np.cos(theta) * dt
        y += v * np.sin(theta) * dt
        theta += (v / L) * np.tan(delta) * dt
        
        X.append(x)
        Y.append(y)
        
    plt.plot(X, Y, label=caso["label"], color=caso["color"], linewidth=2.2)

# Elementos de referencia
plt.scatter([0.0], [0.0], color='black', marker='o', s=100, zorder=5, label="Inicio común (0, 0)")
plt.scatter(goal[0], goal[1], color='red', marker='x', s=140, linewidths=3, zorder=5, label="Meta (5, 5)")

# Configuración estricta de límites dentro del área requerida
plt.xlim(0.0, 8.0)
plt.ylim(0.0, 8.0)
plt.title("Parte 2: Cinco Trayectorias hacia el Punto Objetivo en [0, 10] x [0, 10]", fontsize=12)
plt.xlabel("X [m]", fontsize=11)
plt.ylabel("Y [m]", fontsize=11)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend(loc="upper right", fontsize=9.5)
plt.tight_layout()
plt.show()