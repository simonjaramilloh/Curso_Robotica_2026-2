import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from roboticstoolbox.tools.trajectory import jtraj

L1, L2 = 0.6, 0.4
q0 = np.deg2rad([-30, 60])
qf = np.deg2rad([110, -90])

pasos = 125
t5 = np.linspace(0, 5.0, pasos)
t3 = np.linspace(0, 3.0, int(pasos * 3 / 5))

traj5 = jtraj(q0, qf, t5)
traj3 = jtraj(q0, qf, t3)

# Rellenar traj3 para mantener la posición final de 3s a 5s
q3_full = np.vstack((traj3.q, np.tile(qf, (pasos - len(t3), 1))))
qd3_full = np.vstack((traj3.qd, np.zeros((pasos - len(t3), 2))))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

b5_line, = ax1.plot([], [], 'o-', color='#1f77b4', linewidth=3, label="Robot T = 5.0s")
b3_line, = ax1.plot([], [], 'o--', color='#d62728', linewidth=3, label="Robot T = 3.0s (Rápido)")
ax1.set_xlim(-1.0, 1.1)
ax1.set_ylim(-0.8, 1.1)
ax1.set_aspect('equal')
ax1.grid(True, linestyle="--", alpha=0.7)
ax1.set_title("Carrera Cartesiana: T=3s vs T=5s")
ax1.set_xlabel("X [m]")
ax1.set_ylabel("Y [m]")
ax1.legend(loc="lower left")

ax2.plot(t5, np.rad2deg(traj5.qd[:, 0]), 'b-', alpha=0.3, label="qd1 (T=5s)")
ax2.plot(t3, np.rad2deg(traj3.qd[:, 0]), 'r-', alpha=0.3, label="qd1 (T=3s)")
c5_line, = ax2.plot([], [], 'b-', linewidth=2.5)
c3_line, = ax2.plot([], [], 'r--', linewidth=2.5)
ax2.set_title("Comparación de Velocidad Articular 1 [°/s]")
ax2.set_xlabel("Tiempo [s]")
ax2.set_ylabel("Velocidad [°/s]")
ax2.grid(True, linestyle="--", alpha=0.7)
ax2.legend()

def update(frame):
    # Robot 5s
    q1_5, q2_5 = traj5.q[frame]
    x1_5, y1_5 = L1*np.cos(q1_5), L1*np.sin(q1_5)
    x2_5, y2_5 = x1_5 + L2*np.cos(q1_5+q2_5), y1_5 + L2*np.sin(q1_5+q2_5)
    b5_line.set_data([0, x1_5, x2_5], [0, y1_5, y2_5])
    
    # Robot 3s
    q1_3, q2_3 = q3_full[frame]
    x1_3, y1_3 = L1*np.cos(q1_3), L1*np.sin(q1_3)
    x2_3, y2_3 = x1_3 + L2*np.cos(q1_3+q2_3), y1_3 + L2*np.sin(q1_3+q2_3)
    b3_line.set_data([0, x1_3, x2_3], [0, y1_3, y2_3])
    
    c5_line.set_data(t5[:frame+1], np.rad2deg(traj5.qd[:frame+1, 0]))
    c3_line.set_data(t5[:frame+1], np.rad2deg(qd3_full[:frame+1, 0]))
    return b5_line, b3_line, c5_line, c3_line

ani = FuncAnimation(fig, update, frames=pasos, interval=40, blit=True)
print("Guardando p4_var1.gif...")
ani.save("p4_var1.gif", writer="pillow", fps=25)
print("¡GIF guardado con éxito!")
plt.show()