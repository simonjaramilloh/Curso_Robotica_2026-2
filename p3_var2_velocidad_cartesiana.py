import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L1, L2 = 0.6, 0.4
qd = np.array([0.5, 1.5]) # Velocidades articulares constantes [rad/s]

pasos = 120
t = np.linspace(0, 4.0, pasos)
q1_t = 0.2 + qd[0] * t
q2_t = -1.5 + qd[1] * t

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

brazo_line, = ax1.plot([], [], 'o-', color='#2ca02c', linewidth=3, markersize=8, label="Robot 2R")
vel_vec, = ax1.plot([], [], 'r-', linewidth=2.5, label="Vector velocidad v_E")
vel_punta, = ax1.plot([], [], 'r^', markersize=7)
ax1.set_xlim(-1.1, 1.1)
ax1.set_ylim(-1.1, 1.1)
ax1.set_aspect('equal')
ax1.grid(True, linestyle="--", alpha=0.7)
ax1.set_title("Vector Velocidad Cartesiana v = J(q)·q_dot")
ax1.set_xlabel("X [m]")
ax1.set_ylabel("Y [m]")
ax1.legend(loc="lower left")

ax2.set_xlim(0, 4.0)
ax2.set_ylim(0, 1.8)
linea_mag, = ax2.plot([], [], 'm-', linewidth=2, label="||v_E|| [m/s]")
ax2.set_title("Magnitud de Velocidad del Efector Final")
ax2.set_xlabel("Tiempo [s]")
ax2.set_ylabel("Rapidez [m/s]")
ax2.grid(True, linestyle="--", alpha=0.7)
ax2.legend()

hist_t, hist_v = [], []

def update(frame):
    q1, q2 = q1_t[frame], q2_t[frame]
    x1, y1 = L1 * np.cos(q1), L1 * np.sin(q1)
    x2, y2 = x1 + L2 * np.cos(q1 + q2), y1 + L2 * np.sin(q1 + q2)
    brazo_line.set_data([0, x1, x2], [0, y1, y2])
    
    J = np.array([
        [-L1*np.sin(q1) - L2*np.sin(q1+q2), -L2*np.sin(q1+q2)],
        [ L1*np.cos(q1) + L2*np.cos(q1+q2),  L2*np.cos(q1+q2)]
    ])
    v = J @ qd
    escala = 0.35
    vel_vec.set_data([x2, x2 + escala * v[0]], [y2, y2 + escala * v[1]])
    vel_punta.set_data([x2 + escala * v[0]], [y2 + escala * v[1]])
    
    hist_t.append(t[frame])
    hist_v.append(np.linalg.norm(v))
    linea_mag.set_data(hist_t, hist_v)
    return brazo_line, vel_vec, vel_punta, linea_mag

ani = FuncAnimation(fig, update, frames=pasos, interval=45, blit=True)
print("Guardando p3_var2.gif...")
ani.save("p3_var2.gif", writer="pillow", fps=22)
print("¡GIF guardado con éxito!")
plt.show()