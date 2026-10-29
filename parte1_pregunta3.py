import numpy as np
import matplotlib.pyplot as plt

# Parámetros fijos
v = 1.0              # Velocidad lineal longitudinal [m/s]
delta = 0.3          # Ángulo de viraje [rad]
dt = 0.1             # Paso de integración [s]

# 3 Valores de longitud entre ejes (wheelbase) a contrastar
valores_L = [1.0, 2.0, 3.0]
colores = ['#2ca02c', '#1f77b4', '#d62728']

plt.figure(figsize=(9, 9))

for L, color in zip(valores_L, colores):
    # Cálculo analítico del radio de curvatura e ICR
    R = L / np.tan(delta)
    icr_x, icr_y = 0.0, R
    
    # Tiempo de una revolución completa (2*pi radianes)
    theta_dot = (v / L) * np.tan(delta)
    T = (2.0 * np.pi) / theta_dot
    pasos = int(np.ceil(T / dt))
    
    # Simulación e integración numérica
    x, y, theta = 0.0, 0.0, 0.0
    X, Y = [x], [y]
    
    for _ in range(pasos):
        x_dot = v * np.cos(theta)
        y_dot = v * np.sin(theta)
        theta_dot_step = (v / L) * np.tan(delta)
        
        x += x_dot * dt
        y += y_dot * dt
        theta += theta_dot_step * dt
        
        X.append(x)
        Y.append(y)
        
    # Graficar trayectoria orbital y su respectivo centro de curvatura ICR
    plt.plot(X, Y, color=color, linewidth=2, 
             label=f"L = {L:.1f} m  ->  $R_B$ = {R:.2f} m")
    plt.scatter([icr_x], [icr_y], color=color, marker='+', s=120)

# Punto de partida común
plt.scatter([0.0], [0.0], color='black', marker='o', s=90, zorder=5, label="Inicio común (0, 0)")

plt.title("Efecto de la Longitud entre Ejes $L$ en el Radio de Curvatura", fontsize=13)
plt.xlabel("X [m]", fontsize=11)
plt.ylabel("Y [m]", fontsize=11)
plt.axis('equal')
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend(loc="upper right", fontsize=10)
plt.tight_layout()
plt.show()