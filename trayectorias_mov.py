import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from roboticstoolbox.tools.trajectory import jtraj

print("--- PARTE 4: GENERACIÓN DE TRAYECTORIAS ---")

L1 = 0.6
L2 = 0.4

q0 = np.deg2rad([0, 0])
qf = np.deg2rad([60, -45])

T = 5.0
pasos = 125
t = np.linspace(0, T, pasos)

traj = jtraj(q0, qf, t)
q = traj.q
qd = traj.qd
qdd = traj.qdd

q1 = q[:, 0]
q2 = q[:, 1]
x = L1 * np.cos(q1) + L2 * np.cos(q1 + q2)
y = L1 * np.sin(q1) + L2 * np.sin(q1 + q2)

fig = plt.figure(figsize=(13, 8))
gs = fig.add_gridspec(3, 2, width_ratios=[1.1, 1.2])

ax_pos = fig.add_subplot(gs[0, 0])
ax_vel = fig.add_subplot(gs[1, 0])
ax_acc = fig.add_subplot(gs[2, 0])
ax_cart = fig.add_subplot(gs[:, 1])

# Configurar paneles articulares (Actividad 4.1)
axes_art = [ax_pos, ax_vel, ax_acc]
datos = [q, qd, qdd]
titulos = ["Posiciones articulares", "Velocidades articulares", "Aceleraciones articulares"]
unidades = ["Posición [°]", "Velocidad [°/s]", "Aceleración [°/s²]"]

lineas_q1, lineas_q2 = [], []
for ax, valores, titulo, unidad in zip(axes_art, datos, titulos, unidades):
    ax.plot(t, np.rad2deg(valores[:, 0]), color='#1f77b4', alpha=0.25)
    ax.plot(t, np.rad2deg(valores[:, 1]), color='#ff7f0e', alpha=0.25)
    l1, = ax.plot([], [], color='#1f77b4', linewidth=2, label="Articulación 1")
    l2, = ax.plot([], [], color='#ff7f0e', linewidth=2, label="Articulación 2")
    lineas_q1.append(l1)
    lineas_q2.append(l2)
    ax.set_title(titulo, fontsize=10)
    ax.set_xlabel("Tiempo [s]", fontsize=9)
    ax.set_ylabel(unidad, fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend(loc="upper right", fontsize=8)

# Configurar panel cartesiano (Actividad 4.2)
ax_cart.plot([x[0], x[-1]], [y[0], y[-1]], 'r--', linewidth=2, label="Segmento recto ideal")
ax_cart.scatter(x[0], y[0], color='green', s=90, zorder=5, label="Inicio (q0)")
ax_cart.scatter(x[-1], y[-1], color='red', s=90, zorder=5, label="Final (qf)")
rastro_cart, = ax_cart.plot([], [], 'b-', linewidth=3, label="Trayectoria cartesiana real")
brazo_cart, = ax_cart.plot([], [], 'o-', color='#2ca02c', linewidth=3, markersize=8, label="Manipulador 2R")

ax_cart.set_xlabel("X [m]")
ax_cart.set_ylabel("Y [m]")
ax_cart.set_title(f"Trayectoria del Efector Final (T = {T}s)")
ax_cart.set_aspect("equal")
ax_cart.set_xlim(-0.1, 1.15)
ax_cart.set_ylim(-0.1, 1.15)
ax_cart.grid(True, linestyle="--", alpha=0.7)
ax_cart.legend(loc="lower left")

plt.tight_layout()

def update(frame):
    t_sub = t[:frame+1]
    for idx, valores in enumerate(datos):
        lineas_q1[idx].set_data(t_sub, np.rad2deg(valores[:frame+1, 0]))
        lineas_q2[idx].set_data(t_sub, np.rad2deg(valores[:frame+1, 1]))
        
    x1 = L1 * np.cos(q1[frame])
    y1 = L1 * np.sin(q1[frame])
    brazo_cart.set_data([0, x1, x[frame]], [0, y1, y[frame]])
    rastro_cart.set_data(x[:frame+1], y[:frame+1])
    
    return lineas_q1 + lineas_q2 + [brazo_cart, rastro_cart]

ani = FuncAnimation(fig, update, frames=pasos, interval=40, blit=True)
print("Guardando trayectorias_mov.gif...")
ani.save("trayectorias_mov.gif", writer="pillow", fps=25)
print("¡GIF guardado!")
plt.show()