import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L1, L2 = 0.6, 0.4
r_min, r_max = abs(L1 - L2), L1 + L2

pasos = 110
xd_t = np.linspace(0.05, 1.15, pasos)
yd_t = np.linspace(0.05, 0.40, pasos)

fig, ax = plt.subplots(figsize=(7, 7))
theta = np.linspace(0, 2 * np.pi, 300)
ax.plot(r_max * np.cos(theta), r_max * np.sin(theta), 'k--', alpha=0.4, label="R_max (1.0m)")
ax.plot(r_min * np.cos(theta), r_min * np.sin(theta), 'r--', alpha=0.4, label="R_min (0.2m)")

brazo_line, = ax.plot([], [], 'o-', color='#1f77b4', linewidth=3, markersize=8, label="Robot 2R")
obj_point, = ax.plot([], [], 'ro', markersize=9, label="Objetivo deseado")
estado_txt = ax.text(-0.2, 1.02, '', fontsize=11, fontweight='bold')

ax.set_xlim(-0.3, 1.25)
ax.set_ylim(-0.3, 1.2)
ax.set_aspect('equal')
ax.grid(True, linestyle="--", alpha=0.7)
ax.set_title("Variante 2.2: Objetivo entrando y saliendo del Espacio de Trabajo")
ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.legend(loc="lower right")

def update(frame):
    xd, yd = xd_t[frame], yd_t[frame]
    c2 = (xd**2 + yd**2 - L1**2 - L2**2) / (2 * L1 * L2)
    
    if abs(c2) > 1.0:
        estado_txt.set_text(f"Estado: INALCANZABLE (|c2|={abs(c2):.2f} > 1)")
        estado_txt.set_color('#d62728')
        c2_clip = np.clip(c2, -1.0, 1.0)
        brazo_line.set_color('#7f7f7f')
    else:
        estado_txt.set_text(f"Estado: ALCANZABLE (|c2|={abs(c2):.2f} <= 1)")
        estado_txt.set_color('#2ca02c')
        c2_clip = c2
        brazo_line.set_color('#1f77b4')
        
    q2 = np.arccos(c2_clip)
    q1 = np.arctan2(yd, xd) - np.arctan2(L2 * np.sin(q2), L1 + L2 * np.cos(q2))
    x1, y1 = L1 * np.cos(q1), L1 * np.sin(q1)
    x2, y2 = x1 + L2 * np.cos(q1 + q2), y1 + L2 * np.sin(q1 + q2)
    
    brazo_line.set_data([0, x1, x2], [0, y1, y2])
    obj_point.set_data([xd], [yd])
    return brazo_line, obj_point, estado_txt

ani = FuncAnimation(fig, update, frames=pasos, interval=50, blit=True)
print("Guardando p2_var2.gif...")
ani.save("p2_var2.gif", writer="pillow", fps=20)
print("¡GIF guardado con éxito!")
plt.show()