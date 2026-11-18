import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import ET2

# Parámetros del manipulador
L1 = 0.6
L2 = 0.4

# Modelo cinemático con transformaciones elementales
robot = (
    ET2.R() * ET2.tx(L1) * ET2.R() * ET2.tx(L2)
)

# Definir las 4 configuraciones (en grados y pasadas a radianes)
configuraciones = {
    'A': np.deg2rad([0, 0]),
    'B': np.deg2rad([30, 45]),
    'C': np.deg2rad([60, -30]),
    'D': np.deg2rad([90, 90])
}

colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

plt.figure(figsize=(8, 8))

# --- ACTIVIDAD 1.1: Graficar configuraciones y calcular Cinemática Directa ---
print("--- POSES DEL EFECTOR FINAL (Cinemática Directa) ---")
for (nombre, q), color in zip(configuraciones.items(), colores):
    # Calcular y mostrar la transformación homogénea
    T = robot.fkine(q)
    print(f"\nConfiguración {nombre} (q1={np.rad2deg(q[0]):.0f}°, q2={np.rad2deg(q[1]):.0f}°):")
    print(T)
    
    # Coordenadas de los eslabones para la gráfica
    x0, y0 = 0.0, 0.0
    x1 = L1 * np.cos(q[0])
    y1 = L1 * np.sin(q[0])
    x2 = x1 + L2 * np.cos(q[0] + q[1])
    y2 = y1 + L2 * np.sin(q[0] + q[1])
    
    # Graficar el brazo
    plt.plot([x0, x1, x2], [y0, y1, y2], 'o-', color=color, linewidth=3, markersize=8, 
             label=f"Config. {nombre} ({np.rad2deg(q[0]):.0f}°, {np.rad2deg(q[1]):.0f}°)")

# --- ACTIVIDAD 1.2: Espacio de Trabajo ---
# Cálculo de los radios mínimo y máximo
r_min = abs(L1 - L2)
r_max = L1 + L2

theta = np.linspace(0, 2*np.pi, 500)

# Graficar límites
plt.plot(r_max * np.cos(theta), r_max * np.sin(theta), 'k--', alpha=0.5, label="Límite exterior")
plt.plot(r_min * np.cos(theta), r_min * np.sin(theta), 'r--', alpha=0.5, label="Límite interior (Singularidad)")

# Configuraciones de la gráfica
plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.title("Actividad 1: Configuraciones y Espacio de Trabajo (Manipulador 2R)")
plt.axis("equal")
plt.xlim(-1.2, 1.2)
plt.ylim(-1.2, 1.2)
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend(loc="upper right", fontsize=9)

plt.show()