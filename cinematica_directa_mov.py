import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from roboticstoolbox import ET2

# Longitudes originales de los eslabones
L1 = 0.6
L2 = 0.4

# Modelo cinemático con transformaciones elementales
robot = ET2.R() * ET2.tx(L1) * ET2.R() * ET2.tx(L2)

# Configuración articular objetivo original
q_obj = np.deg2rad([30, 45])

# Cinemática directa con Robotics Toolbox
T = robot.fkine(q_obj)
print("Transformación homogénea en q = [30°, 45°]:")
print(T)

# Vector de interpolación temporal desde [0°, 0°] hasta [30°, 45°]
pasos = 80
q1_t = np.linspace(0, q_obj[0], pasos)
q2_t = np.linspace(0, q_obj[1], pasos)

fig, ax = plt.subplots(figsize=(7, 7))
brazo_line, = ax.plot([], [], "o-", color="#1f77b4", linewidth=3, markersize=8, label="Manipulador 2R")
rastro_line, = ax.plot([], [], "--", color="#ff7f0e", linewidth=1.5, label="Trayectoria efector")
texto_info = ax.text(-1.0, 0.9, '', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.set_title("Manipulador plano 2R (Transición a 30°, 45°)")
ax.grid(True, linestyle="--", alpha=0.7)
ax.set_aspect("equal")
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.legend(loc="lower right")

hx, hy = [], []

def update(frame):
    q1, q2 = q1_t[frame], q2_t[frame]
    x1, y1 = L1 * np.cos(q1), L1 * np.sin(q1)
    x2, y2 = x1 + L2 * np.cos(q1 + q2), y1 + L2 * np.sin(q1 + q2)
    
    brazo_line.set_data([0.0, x1, x2], [0.0, y1, y2])
    hx.append(x2); hy.append(y2)
    rastro_line.set_data(hx, hy)
    texto_info.set_text(f"q1: {np.rad2deg(q1):.1f}° | q2: {np.rad2deg(q2):.1f}°\nEfector: ({x2:.3f}, {y2:.3f}) m")
    return brazo_line, rastro_line, texto_info

ani = FuncAnimation(fig, update, frames=pasos, interval=40, blit=True)
print("Guardando cinematica_directa_mov.gif...")
ani.save("cinematica_directa_mov.gif", writer="pillow", fps=25)
print("¡GIF guardado!")
plt.show()