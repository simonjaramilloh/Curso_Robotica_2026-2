import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L1 = 0.6
L2 = 0.4

puntos = {
    'A': (0.5, 0.5),
    'B': (0.95, 0.10),
    'C': (1.20, 0.20)
}

print("--- PARTE 2: CINEMÁTICA INVERSA ---")
soluciones_A = []

for nombre, (xd, yd) in puntos.items():
    print(f"\nEvaluando Punto {nombre}: (X={xd}m, Y={yd}m)")
    c2 = (xd**2 + yd**2 - L1**2 - L2**2) / (2 * L1 * L2)
    
    if abs(c2) > 1:
        print("  -> RESULTADO: Posición NO alcanzable (Fuera del espacio de trabajo)")
    else:
        print("  -> RESULTADO: Posición ALCANZABLE")
        q2_a = np.arccos(c2)
        q2_b = -np.arccos(c2)
        
        soluciones = []
        for q2 in [q2_a, q2_b]:
            q1 = np.arctan2(yd, xd) - np.arctan2(L2 * np.sin(q2), L1 + L2 * np.cos(q2))
            soluciones.append([q1, q2])
            
        if nombre == 'A':
            soluciones_A = soluciones
            
        for i, (q1, q2) in enumerate(soluciones):
            x = L1 * np.cos(q1) + L2 * np.cos(q1 + q2)
            y = L1 * np.sin(q1) + L2 * np.sin(q1 + q2)
            error = np.hypot(xd - x, yd - y)
            print(f"  Solución {i+1}:")
            print(f"    Articulaciones [°]: q1 = {np.rad2deg(q1):.2f}°, q2 = {np.rad2deg(q2):.2f}°")
            print(f"    Posición verificada: ({x:.4f}, {y:.4f})")
            print(f"    Error (ep): {error:.4e} m")

# Animación de las dos soluciones hacia el Punto A (0.5, 0.5)
pasos = 90
q_sol1 = np.linspace([0, 0], soluciones_A[0], pasos)
q_sol2 = np.linspace([0, 0], soluciones_A[1], pasos)

fig, ax = plt.subplots(figsize=(8, 8))
ax.plot(puntos['A'][0], puntos['A'][1], 'rx', markersize=12, markeredgewidth=3, label="Punto Objetivo A (0.5, 0.5)")

brazo1, = ax.plot([], [], 'o-', color='#1f77b4', linewidth=3, markersize=8, label="Solución 1 (Codo Abajo)")
brazo2, = ax.plot([], [], 'o-', color='#ff7f0e', linewidth=3, markersize=8, label="Solución 2 (Codo Arriba)")
rastro1, = ax.plot([], [], ':', color='#1f77b4', linewidth=1.5)
rastro2, = ax.plot([], [], ':', color='#ff7f0e', linewidth=1.5)

ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.set_title("Actividad 2.1: Convergencia de Múltiples Soluciones de Cinemática Inversa")
ax.grid(True, linestyle="--", alpha=0.7)
ax.set_aspect("equal")
ax.set_xlim(-0.2, 1.2)
ax.set_ylim(-0.2, 1.2)
ax.legend(loc="lower right")

h1x, h1y, h2x, h2y = [], [], [], []

def update(frame):
    # Solución 1
    q1_1, q2_1 = q_sol1[frame]
    x1_1, y1_1 = L1 * np.cos(q1_1), L1 * np.sin(q1_1)
    x2_1, y2_1 = x1_1 + L2 * np.cos(q1_1 + q2_1), y1_1 + L2 * np.sin(q1_1 + q2_1)
    brazo1.set_data([0, x1_1, x2_1], [0, y1_1, y2_1])
    h1x.append(x2_1); h1y.append(y2_1)
    rastro1.set_data(h1x, h1y)
    
    # Solución 2
    q1_2, q2_2 = q_sol2[frame]
    x1_2, y1_2 = L1 * np.cos(q1_2), L1 * np.sin(q1_2)
    x2_2, y2_2 = x1_2 + L2 * np.cos(q1_2 + q2_2), y1_2 + L2 * np.sin(q1_2 + q2_2)
    brazo2.set_data([0, x1_2, x2_2], [0, y1_2, y2_2])
    h2x.append(x2_2); h2y.append(y2_2)
    rastro2.set_data(h2x, h2y)
    
    return brazo1, brazo2, rastro1, rastro2

ani = FuncAnimation(fig, update, frames=pasos, interval=40, blit=True)
print("\nGuardando cinematica_inversa_mov.gif...")
ani.save("cinematica_inversa_mov.gif", writer="pillow", fps=25)
print("¡GIF guardado!")
plt.show()