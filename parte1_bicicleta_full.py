import numpy as np
import matplotlib.pyplot as plt

# Parámetros del modelo
L = 2.0         # Wheelbase [m]
v = 1.0         # Velocidad longitudinal [m/s]
delta = 0.3     # Ángulo de dirección [rad]
dt = 0.1        # Paso de integración [s]

# 1. Cálculo del tiempo y pasos para 2*pi radianes
theta_dot_const = (v / L) * np.tan(delta)
T = (2.0 * np.pi) / theta_dot_const   # Periodo total (~40.62 s)
pasos = int(np.ceil(T / dt))         # ~407 pasos

# Radio y Centro analítico del círculo (para verificación)
R = L / np.tan(delta)                 # Radio ~6.46 m
# Como el robot sale de (0,0) con theta=0 apuntando a +X y gira a la izquierda (+Y),
# el centro de rotación (ICR) está en (0, R)
x_centro, y_centro = 0.0, R

# Condiciones iniciales
x, y, theta = 0.0, 0.0, 0.0
X, Y = [x], [y]

# Simulación durante toda la revolución
for _ in range(pasos):
    x_dot = v * np.cos(theta)
    y_dot = v * np.sin(theta)
    theta_dot = (v / L) * np.tan(delta)
    
    x += x_dot * dt
    y += y_dot * dt
    theta += theta_dot * dt
    
    X.append(x)
    Y.append(y)

# Graficación
plt.figure(figsize=(8, 8))
plt.plot(X, Y, 'b-', linewidth=2, label="Trayectoria simulada (Bicicleta)")
plt.scatter([0], [0], color='green', marker='o', s=80, label="Inicio / Fin (0,0)")
plt.scatter([x_centro], [y_centro], color='red', marker='+', s=100, label=f"Centro ICR (0, {R:.2f})")
# --- Añadir después de plt.scatter(...) ---
# Segmento del radio desde el ICR (0, R) hasta el origen (0, 0)
plt.plot([x_centro, 0.0], [y_centro, 0.0], 'k--', linewidth=1.5, label=f"Radio $R_B = {R:.2f}\\,\\mathrm{{m}}$")

# Texto con la cota del radio
plt.text(0.2, y_centro / 2.0, f"$R_B = {R:.2f}\\,\\mathrm{{m}}$", fontsize=11, color='black', weight='bold')

plt.title("Parte 1: Circunferencia Completa (Revolución $2\\pi$)")
plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.show()