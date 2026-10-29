import numpy as np
import matplotlib.pyplot as plt

# Parámetros del modelo
L = 2.0         # Distancia entre ejes (wheelbase) [m]
v = 1.0         # Velocidad longitudinal [m/s]
delta = 0.3     # Ángulo de dirección [rad]

# Condiciones iniciales
x, y, theta = 0.0, 0.0, 0.0
dt = 0.1        # Paso de integración [s]

X, Y = [], []

# Simulación durante 100 pasos de tiempo (10 segundos)
for _ in range(100):
    x_dot = v * np.cos(theta)
    y_dot = v * np.sin(theta)
    theta_dot = (v / L) * np.tan(delta)
    
    # Integración numérica (Euler hacia adelante)
    x += x_dot * dt
    y += y_dot * dt
    theta += theta_dot * dt
    
    X.append(x)
    Y.append(y)

# Graficación
plt.figure(figsize=(7, 7))
plt.plot(X, Y, 'b-', linewidth=2, label="Trayectoria del robot")
plt.title("Parte 1: Modelo Cinemático (Bicicleta)")
plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.show()