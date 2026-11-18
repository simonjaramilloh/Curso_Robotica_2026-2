import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L1, L2 = 0.6, 0.4
pasos = 100
ang = np.linspace(0, 2 * np.pi, pasos)

# Circunferencia objetivo de radio 0.22m centrada en (-0.45, 0.45)
xd_t = -0.45 + 0.22 * np.cos(ang)
yd_t =  0.45 + 0.22 * np.sin(ang)

fig, ax = plt.subplots(figsize=(7, 7))
ax.plot(xd_t, yd_t, 'k--', linewidth=1.5, label="Trayectoria objetivo")
punto_obj, = ax.plot([], [], 'rx', markersize=10, markeredgewidth=2, label="Objetivo (xd, yd)")
brazo_abajo, = ax.plot([], [], 'o-', color='#1f77b4', linewidth=3, label="Solución 1 (Codo Abajo)")
brazo_arriba, = ax.plot([], [], 'o--', color='#ff7f0e', linewidth=3, label="Solución 2 (Codo Arriba)")

ax.set_xlim(-1.0, 0.4)
ax.set_ylim(-0.2, 1.0)
ax.set_aspect('equal')
ax.grid(True, linestyle="--", alpha=0.7)
ax.set_title("Variante 2.1: Cinemática Inversa Continua (2 Soluciones)")
ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.legend(loc="lower right")

def resolver_ik(xd, yd, signo=1):
    c2 = np.clip((xd**2 + yd**2 - L1**2 - L2**2) / (2 * L1 * L2), -1.0, 1.0)
    q2 = signo * np.arccos(c2)
    q1 = np.arctan2(yd, xd) - np.arctan2(L2 * np.sin(q2), L1 + L2 * np.cos(q2))
    return q1, q2

def update(frame):
    xd, yd = xd_t[frame], yd_t[frame]
    punto_obj.set_data([xd], [yd])
    
    q1_a, q2_a = resolver_ik(xd, yd, +1)
    x1_a, y1_a = L1 * np.cos(q1_a), L1 * np.sin(q1_a)
    brazo_abajo.set_data([0, x1_a, xd], [0, y1_a, yd])
    
    q1_b, q2_b = resolver_ik(xd, yd, -1)
    x1_b, y1_b = L1 * np.cos(q1_b), L1 * np.sin(q1_b)
    brazo_arriba.set_data([0, x1_b, xd], [0, y1_b, yd])
    
    return punto_obj, brazo_abajo, brazo_arriba

ani = FuncAnimation(fig, update, frames=pasos, interval=45, blit=True)
print("Guardando p2_var1.gif...")
ani.save("p2_var1.gif", writer="pillow", fps=22)
print("¡GIF guardado con éxito!")
plt.show()