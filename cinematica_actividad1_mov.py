import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from roboticstoolbox import ET2

L1 = 0.6
L2 = 0.4
robot = ET2.R() * ET2.tx(L1) * ET2.R() * ET2.tx(L2)

# Configuraciones originales de la Actividad 1.1
configuraciones = {
    'A': np.deg2rad([0, 0]),
    'B': np.deg2rad([30, 45]),
    'C': np.deg2rad([60, -30]),
    'D': np.deg2rad([90, 90])
}
nombres = list(configuraciones.keys())
q_lista = list(configuraciones.values())
colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

print("--- POSES DEL EFECTOR FINAL (Cinemática Directa) ---")
for nombre, q in configuraciones.items():
    print(f"\nConfiguración {nombre} (q1={np.rad2deg(q[0]):.0f}°, q2={np.rad2deg(q[1]):.0f}°):")
    print(robot.fkine(q))

# Construir secuencia de animación entre A -> B -> C -> D
pasos_tramo = 35
q_seq = []
for i in range(len(q_lista) - 1):
    q_tramo = np.linspace(q_lista[i], q_lista[i+1], pasos_tramo)
    q_seq.append(q_tramo)
q_seq = np.vstack(q_seq)
total_frames = len(q_seq)

r_min = abs(L1 - L2)
r_max = L1 + L2
theta = np.linspace(0, 2 * np.pi, total_frames)

fig, ax = plt.subplots(figsize=(8, 8))
lim_ext, = ax.plot([], [], 'k--', alpha=0.5, label="Límite exterior (1.0m)")
lim_int, = ax.plot([], [], 'r--', alpha=0.5, label="Límite interior (0.2m)")

# Líneas estáticas que se activan al alcanzar cada configuración
lineas_fijas = []
for nombre, q, col in zip(nombres, q_lista, colores):
    ln, = ax.plot([], [], 'o-', color=col, linewidth=2.5, markersize=7, alpha=0.65,
                  label=f"Config. {nombre} ({np.rad2deg(q[0]):.0f}°, {np.rad2deg(q[1]):.0f}°)")
    lineas_fijas.append(ln)

brazo_activo, = ax.plot([], [], 'o-', color='black', linewidth=3.5, markersize=8, label="Brazo en movimiento")

ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.set_title("Actividad 1: Configuraciones A, B, C, D y Espacio de Trabajo")
ax.set_aspect("equal")
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.grid(True, linestyle="--", alpha=0.7)
ax.legend(loc="upper right", fontsize=8.5)

def coords_brazo(q):
    x1, y1 = L1 * np.cos(q[0]), L1 * np.sin(q[0])
    x2, y2 = x1 + L2 * np.cos(q[0] + q[1]), y1 + L2 * np.sin(q[0] + q[1])
    return [0, x1, x2], [0, y1, y2]

def update(frame):
    # Trazar progresivamente los círculos del espacio de trabajo
    th = theta[:frame+1]
    lim_ext.set_data(r_max * np.cos(th), r_max * np.sin(th))
    lim_int.set_data(r_min * np.cos(th), r_min * np.sin(th))
    
    # Mover el brazo activo
    q_act = q_seq[frame]
    bx, by = coords_brazo(q_act)
    brazo_activo.set_data(bx, by)
    
    # Fijar las posturas A, B, C, D conforme se alcanzan
    hitos = [0, pasos_tramo - 1, 2 * pasos_tramo - 1, 3 * pasos_tramo - 1]
    for idx, hito in enumerate(hitos):
        if frame >= hito:
            fx, fy = coords_brazo(q_lista[idx])
            lineas_fijas[idx].set_data(fx, fy)
            
    return [lim_ext, lim_int, brazo_activo] + lineas_fijas

ani = FuncAnimation(fig, update, frames=total_frames, interval=40, blit=True)
print("\nGuardando cinematica_actividad1_mov.gif...")
ani.save("cinematica_actividad1_mov.gif", writer="pillow", fps=25)
print("¡GIF guardado!")
plt.show()