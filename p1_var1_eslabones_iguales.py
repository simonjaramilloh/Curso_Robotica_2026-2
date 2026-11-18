import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Variante 1.1: Eslabones iguales (r_min = 0)
L1, L2 = 0.5, 0.5
r_min, r_max = abs(L1 - L2), L1 + L2

# Barrido temporal: q1 gira 360° mientras q2 se pliega de 0° a 180°
pasos = 120
q1_t = np.linspace(0, 2 * np.pi, pasos)
q2_t = np.linspace(0, np.pi, pasos)

fig, ax = plt.subplots(figsize=(7, 7))
theta = np.linspace(0, 2 * np.pi, 300)
ax.plot(r_max * np.cos(theta), r_max * np.sin(theta), 'k--', alpha=0.5, label=f"Límite exterior ({r_max:.1f}m)")
ax.plot(0, 0, 'rx', markersize=10, label=f"Límite interior (r_min={r_min:.1f}m)")

brazo_line, = ax.plot([], [], 'o-', color='#1f77b4', linewidth=3, markersize=8, label="Manipulador 2R")
rastro_line, = ax.plot([], [], '-', color='#ff7f0e', linewidth=1.5, alpha=0.8, label="Rastro efector")
texto_info = ax.text(-1.0, 0.95, '', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)
ax.set_aspect('equal')
ax.grid(True, linestyle="--", alpha=0.7)
ax.set_title("Variante 1.1: Eslabones Iguales (L1=0.5m, L2=0.5m)")
ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.legend(loc="lower right")

hx, hy = [], []

def update(frame):
    q1, q2 = q1_t[frame], q2_t[frame]
    x1, y1 = L1 * np.cos(q1), L1 * np.sin(q1)
    x2, y2 = x1 + L2 * np.cos(q1 + q2), y1 + L2 * np.sin(q1 + q2)
    
    brazo_line.set_data([0, x1, x2], [0, y1, y2])
    hx.append(x2); hy.append(y2)
    rastro_line.set_data(hx, hy)
    texto_info.set_text(f"q1: {np.rad2deg(q1):.1f}° | q2: {np.rad2deg(q2):.1f}°\nPos: ({x2:.2f}, {y2:.2f}) m")
    return brazo_line, rastro_line, texto_info

ani = FuncAnimation(fig, update, frames=pasos, interval=40, blit=True)
print("Guardando p1_var1.gif...")
ani.save("p1_var1.gif", writer="pillow", fps=25)
print("¡GIF guardado con éxito!")
plt.show()
