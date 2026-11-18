import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.tools.trajectory import jtraj

print("--- PARTE 4: GENERACIÓN DE TRAYECTORIAS ---")

# Parámetros del robot
L1 = 0.6
L2 = 0.4

# Configuraciones articulares inicial y final
q0 = np.deg2rad([0, 0])
qf = np.deg2rad([60, -45])

# Tiempo total del movimiento
T = 5.0
t = np.linspace(0, T, 251)

# --- Actividad 4.1: Trayectorias articulares (Interpolación de 5to orden) ---
traj = jtraj(q0, qf, t)
q = traj.q
qd = traj.qd
qdd = traj.qdd

# Gráficas articulares
fig, axes = plt.subplots(3, 1, figsize=(8, 9))
datos = [q, qd, qdd]
titulos = ["Posiciones articulares", "Velocidades articulares", "Aceleraciones articulares"]
unidades = ["Posición [°]", "Velocidad [°/s]", "Aceleración [°/s²]"]

for ax, valores, titulo, unidad in zip(axes, datos, titulos, unidades):
    ax.plot(t, np.rad2deg(valores[:, 0]), linewidth=2, label="Articulación 1")
    ax.plot(t, np.rad2deg(valores[:, 1]), linewidth=2, label="Articulación 2")
    ax.set_title(titulo)
    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel(unidad)
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend()

plt.tight_layout()
plt.show()

# --- Actividad 4.2: Trayectoria cartesiana del efector final ---
q1 = q[:, 0]
q2 = q[:, 1]

# Evaluación de la cinemática directa para cada instante de tiempo
x = L1 * np.cos(q1) + L2 * np.cos(q1 + q2)
y = L1 * np.sin(q1) + L2 * np.sin(q1 + q2)

plt.figure(figsize=(8, 8))
plt.plot(x, y, 'b-', linewidth=3, label="Trayectoria cartesiana real")
plt.plot([x[0], x[-1]], [y[0], y[-1]], 'r--', linewidth=2, label="Segmento recto ideal")
plt.scatter(x[0], y[0], color='green', s=100, zorder=5, label="Inicio (q0)")
plt.scatter(x[-1], y[-1], color='red', s=100, zorder=5, label="Final (qf)")

plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.title(f"Trayectoria del Efector Final (T = {T}s)")
plt.axis("equal")
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend()
plt.show()