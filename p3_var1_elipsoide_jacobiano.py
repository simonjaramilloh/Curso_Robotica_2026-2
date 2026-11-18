import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L1, L2 = 0.6, 0.4
pasos = 120
q1_fijo = np.deg2rad(35)
q2_t = np.linspace(-np.pi, np.pi, pasos)
det_curva = L1 * L2 * np.sin(q2_t)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

# Panel 1: Determinante
ax1.plot(np.rad2deg(q2_t), det_curva, 'b-', linewidth=2)
ax1.axhline(0, color='k', linestyle='--')
punto_det, = ax1.plot([], [], 'ro', markersize=9)
ax1.set_title("Determinante det(J) = L1·L2·sin(q2)")
ax1.set_xlabel("q2 [°]")
ax1.set_ylabel("det(J) [m²]")
ax1.grid(True, linestyle="--", alpha=0.7)

# Panel 2: Brazo y elipsoide de velocidad
brazo_line, = ax2.plot([], [], 'o-', color='#1f77b4', linewidth=3, markersize=8, label="Robot 2R")
elipse_line, = ax2.plot([], [], 'r-', linewidth=2, label="Elipsoide de velocidad")
ax2.set_xlim(-0.4, 1.3)
ax2.set_ylim(-0.4, 1.3)
ax2.set_aspect('equal')
ax2.grid(True, linestyle="--", alpha=0.7)
ax2.set_title("Elipsoide de Manipulabilidad en el Efector")
ax2.set_xlabel("X [m]")
ax2.set_ylabel("Y [m]")
ax2.legend(loc="lower left")

ang_circ = np.linspace(0, 2 * np.pi, 80)
circ_unit = np.vstack((np.cos(ang_circ), np.sin(ang_circ)))

def update(frame):
    q1, q2 = q1_fijo, q2_t[frame]
    det_val = L1 * L2 * np.sin(q2)
    punto_det.set_data([np.rad2deg(q2)], [det_val])
    
    x1, y1 = L1 * np.cos(q1), L1 * np.sin(q1)
    x2, y2 = x1 + L2 * np.cos(q1 + q2), y1 + L2 * np.sin(q1 + q2)
    brazo_line.set_data([0, x1, x2], [0, y1, y2])
    
    J = np.array([
        [-L1*np.sin(q1) - L2*np.sin(q1+q2), -L2*np.sin(q1+q2)],
        [ L1*np.cos(q1) + L2*np.cos(q1+q2),  L2*np.cos(q1+q2)]
    ])
    elipse = 0.25 * (J @ circ_unit)
    elipse_line.set_data(x2 + elipse[0, :], y2 + elipse[1, :])
    return punto_det, brazo_line, elipse_line

ani = FuncAnimation(fig, update, frames=pasos, interval=45, blit=True)
print("Guardando p3_var1.gif...")
ani.save("p3_var1.gif", writer="pillow", fps=22)
print("¡GIF guardado con éxito!")
plt.show()