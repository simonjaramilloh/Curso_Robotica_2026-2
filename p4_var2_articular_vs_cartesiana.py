import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from roboticstoolbox.tools.trajectory import jtraj, quintic

L1, L2 = 0.6, 0.4
q0 = np.deg2rad([10, 20])
qf = np.deg2rad([115, -75])

pasos = 110
t = np.linspace(0, 4.0, pasos)

# 1. Trayectoria en espacio articular (arco curvo)
traj_j = jtraj(q0, qf, t)
xj = L1*np.cos(traj_j.q[:,0]) + L2*np.cos(traj_j.q[:,0] + traj_j.q[:,1])
yj = L1*np.sin(traj_j.q[:,0]) + L2*np.sin(traj_j.q[:,0] + traj_j.q[:,1])

# 2. Trayectoria en línea recta cartesiana con perfil de 5to orden
s = quintic(0, 1, t).q
xc = xj[0] + s * (xj[-1] - xj[0])
yc = yj[0] + s * (yj[-1] - yj[0])

fig, ax = plt.subplots(figsize=(7.5, 7.5))
ax.plot(xj, yj, 'b:', alpha=0.4, label="Camino Articular (jtraj)")
ax.plot(xc, yc, 'r:', alpha=0.4, label="Segmento Recto Cartesiano")

brazo_j, = ax.plot([], [], 'o-', color='#1f77b4', linewidth=3, label="Robot Articular")
brazo_c, = ax.plot([], [], 'o--', color='#d62728', linewidth=3, label="Robot Cartesiano Recto")
rastro_j, = ax.plot([], [], 'b-', linewidth=2)
rastro_c, = ax.plot([], [], 'r-', linewidth=2)

ax.set_xlim(-0.7, 1.1)
ax.set_ylim(-0.2, 1.1)
ax.set_aspect('equal')
ax.grid(True, linestyle="--", alpha=0.7)
ax.set_title("Variante 4.2: Trayectoria Articular vs. Línea Recta Cartesiana")
ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.legend(loc="lower left")

def update(frame):
    # Brazo Articular
    q1, q2 = traj_j.q[frame]
    x1, y1 = L1*np.cos(q1), L1*np.sin(q1)
    brazo_j.set_data([0, x1, xj[frame]], [0, y1, yj[frame]])
    rastro_j.set_data(xj[:frame+1], yj[:frame+1])
    
    # Brazo Cartesiano (IK punto a punto)
    xd, yd = xc[frame], yc[frame]
    c2 = np.clip((xd**2 + yd**2 - L1**2 - L2**2) / (2 * L1 * L2), -1.0, 1.0)
    q2_c = -np.arccos(c2)
    q1_c = np.arctan2(yd, xd) - np.arctan2(L2*np.sin(q2_c), L1 + L2*np.cos(q2_c))
    x1_c, y1_c = L1*np.cos(q1_c), L1*np.sin(q1_c)
    brazo_c.set_data([0, x1_c, xd], [0, y1_c, yd])
    rastro_c.set_data(xc[:frame+1], yc[:frame+1])
    
    return brazo_j, brazo_c, rastro_j, rastro_c

ani = FuncAnimation(fig, update, frames=pasos, interval=40, blit=True)
print("Guardando p4_var2.gif...")
ani.save("p4_var2.gif", writer="pillow", fps=25)
print("¡GIF guardado con éxito!")
plt.show()