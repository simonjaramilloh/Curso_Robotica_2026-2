import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Variante 1.2: Eslabones asimétricos + Límites articulares
L1, L2 = 0.7, 0.25
q1_lim = np.deg2rad([-45, 135])
q2_lim = np.deg2rad([-90, 90])

# Precalcular nube del espacio de trabajo restringido
q1_grid, q2_grid = np.meshgrid(np.linspace(q1_lim[0], q1_lim[1], 45),
                               np.linspace(q2_lim[0], q2_lim[1], 45))
XW = L1 * np.cos(q1_grid) + L2 * np.cos(q1_grid + q2_grid)
YW = L1 * np.sin(q1_grid) + L2 * np.sin(q1_grid + q2_grid)

pasos = 120
t_param = np.linspace(0, 1, pasos)
q1_t = q1_lim[0] + (q1_lim[1] - q1_lim[0]) * t_param
q2_t = q2_lim[1] * np.sin(4 * np.pi * t_param)

fig, ax = plt.subplots(figsize=(7, 7))
theta = np.linspace(0, 2 * np.pi, 300)
ax.plot((L1+L2)*np.cos(theta), (L1+L2)*np.sin(theta), 'k:', alpha=0.3, label="Límite ideal sin topes")
ax.plot(abs(L1-L2)*np.cos(theta), abs(L1-L2)*np.sin(theta), 'r:', alpha=0.3)
ax.scatter(XW, YW, s=4, color='#aec7e8', alpha=0.5, label="Zona alcanzable real")

brazo_line, = ax.plot([], [], 'o-', color='#2ca02c', linewidth=3, markersize=8, label="Manipulador 2R")
rastro_line, = ax.plot([], [], '-', color='#d62728', linewidth=1.5, label="Barrido en fronteras")

ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect('equal')
ax.grid(True, linestyle="--", alpha=0.7)
ax.set_title("Variante 1.2: Espacio de Trabajo con Límites Articulares")
ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.legend(loc="lower left")

hx, hy = [], []

def update(frame):
    q1, q2 = q1_t[frame], q2_t[frame]
    x1, y1 = L1 * np.cos(q1), L1 * np.sin(q1)
    x2, y2 = x1 + L2 * np.cos(q1 + q2), y1 + L2 * np.sin(q1 + q2)
    brazo_line.set_data([0, x1, x2], [0, y1, y2])
    hx.append(x2); hy.append(y2)
    rastro_line.set_data(hx, hy)
    return brazo_line, rastro_line

ani = FuncAnimation(fig, update, frames=pasos, interval=40, blit=True)
print("Guardando p1_var2.gif...")
ani.save("p1_var2.gif", writer="pillow", fps=25)
print("¡GIF guardado con éxito!")
plt.show()