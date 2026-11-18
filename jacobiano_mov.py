import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L1 = 0.6
L2 = 0.4

q1_prueba = np.deg2rad(30)
q2_prueba = np.deg2rad(45)

J = np.array([
    [-L1*np.sin(q1_prueba) - L2*np.sin(q1_prueba+q2_prueba), -L2*np.sin(q1_prueba+q2_prueba)],
    [ L1*np.cos(q1_prueba) + L2*np.cos(q1_prueba+q2_prueba),  L2*np.cos(q1_prueba+q2_prueba)]
])

print("--- PARTE 3: JACOBIANO Y SINGULARIDADES ---")
print("\nJacobiano en q=[30°, 45°]:")
print(J)
print("\nDeterminante del Jacobiano en esa postura:")
print(f"{np.linalg.det(J):.4f} m²")

pasos = 120
q2_values = np.linspace(-np.pi, np.pi, pasos)
det_values = L1 * L2 * np.sin(q2_values)
q1_sing = np.deg2rad(45)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Panel 1: Determinante vs q2
ax1.plot(np.rad2deg(q2_values), det_values, color='#aec7e8', linewidth=1.5)
curva_det, = ax1.plot([], [], 'b-', linewidth=2.5, label="det(J)")
punto_det, = ax1.plot([], [], 'ro', markersize=8)
ax1.axhline(0, color="black", linestyle="--")
ax1.axvline(0, color="red", linestyle=":", alpha=0.6, label="Singularidad (q2=0°)")
ax1.axvline(180, color="purple", linestyle=":", alpha=0.6, label="Singularidad (q2=±180°)")
ax1.axvline(-180, color="purple", linestyle=":", alpha=0.6)
ax1.set_xlabel("q2 [°]")
ax1.set_ylabel("Determinante del jacobiano [m²]")
ax1.set_title("Variación del Determinante")
ax1.grid(True, linestyle="--", alpha=0.7)
ax1.legend(loc="upper left")

# Panel 2: Posturas singulares y barrido del manipulador
x1_s = L1 * np.cos(q1_sing)
y1_s = L1 * np.sin(q1_sing)
ax2.plot([0, x1_s, x1_s + L2*np.cos(q1_sing)], [0, y1_s, y1_s + L2*np.sin(q1_sing)],
         'o--', color='#d62728', linewidth=2, alpha=0.5, label="Estirado (q2 = 0°)")
ax2.plot([0, x1_s, x1_s + L2*np.cos(q1_sing + np.pi)], [0, y1_s, y1_s + L2*np.sin(q1_sing + np.pi)],
         'o--', color='#9467bd', linewidth=2, alpha=0.5, label="Plegado (q2 = 180°)")

brazo_mov, = ax2.plot([], [], 'o-', color='#1f77b4', linewidth=3, markersize=8, label="Brazo en barrido")
ax2.set_xlabel("X [m]")
ax2.set_ylabel("Y [m]")
ax2.set_title("Posturas Singulares en el Espacio")
ax2.set_aspect("equal")
ax2.set_xlim(-0.3, 1.1)
ax2.set_ylim(-0.3, 1.1)
ax2.grid(True, linestyle="--", alpha=0.7)
ax2.legend(loc="lower left")

def update(frame):
    q2 = q2_values[frame]
    curva_det.set_data(np.rad2deg(q2_values[:frame+1]), det_values[:frame+1])
    punto_det.set_data([np.rad2deg(q2)], [det_values[frame]])
    
    x2 = x1_s + L2 * np.cos(q1_sing + q2)
    y2 = y1_s + L2 * np.sin(q1_sing + q2)
    brazo_mov.set_data([0, x1_s, x2], [0, y1_s, y2])
    
    return curva_det, punto_det, brazo_mov

ani = FuncAnimation(fig, update, frames=pasos, interval=40, blit=True)
print("\nGuardando jacobiano_mov.gif...")
ani.save("jacobiano_mov.gif", writer="pillow", fps=25)
print("¡GIF guardado!")
plt.show()