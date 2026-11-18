import numpy as np
import matplotlib.pyplot as plt

# Parámetros del manipulador
L1 = 0.6
L2 = 0.4

# Configuración de prueba de la guía
q1 = np.deg2rad(30)
q2 = np.deg2rad(45)

# Jacobiano de posición
J = np.array([
    [-L1*np.sin(q1) - L2*np.sin(q1+q2), -L2*np.sin(q1+q2)],
    [ L1*np.cos(q1) + L2*np.cos(q1+q2),  L2*np.cos(q1+q2)]
])

print("--- PARTE 3: JACOBIANO Y SINGULARIDADES ---")
print("\nJacobiano en q=[30°, 45°]:")
print(J)
print("\nDeterminante del Jacobiano en esa postura:")
print(f"{np.linalg.det(J):.4f} m²")

# --- Evaluación del determinante vs q2 ---
# El determinante de este robot analíticamente es L1 * L2 * sin(q2)
q2_values = np.linspace(-np.pi, np.pi, 400)
det_values = L1 * L2 * np.sin(q2_values)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Gráfica 1: Comportamiento del Determinante
ax1.plot(np.rad2deg(q2_values), det_values, linewidth=2)
ax1.axhline(0, color="black", linestyle="--")
ax1.axvline(0, color="red", linestyle=":", alpha=0.6, label="Singularidad (q2=0°)")
ax1.axvline(180, color="red", linestyle=":", alpha=0.6, label="Singularidad (q2=\pm180°)")
ax1.axvline(-180, color="red", linestyle=":", alpha=0.6)
ax1.set_xlabel("q2 [°]")
ax1.set_ylabel("Determinante del jacobiano [m²]")
ax1.set_title("Variación del Determinante")
ax1.grid(True, linestyle="--", alpha=0.7)
ax1.legend()

# --- Actividad 3.4: Gráfica de configuraciones singulares ---
# Ocurren cuando q2 = 0° (brazo estirado) o q2 = 180° (brazo plegado)
sing_q2 = [0, np.pi]
colores = ['#d62728', '#9467bd']
etiquetas = ['Estirado (q2 = 0°)', 'Plegado (q2 = 180°)']

q1_sing = np.deg2rad(45) # Fijamos un q1 arbitrario para que sea fácil visualizarlo

for sq2, color, etiqueta in zip(sing_q2, colores, etiquetas):
    x0, y0 = 0.0, 0.0
    x1 = L1 * np.cos(q1_sing)
    y1 = L1 * np.sin(q1_sing)
    x2 = x1 + L2 * np.cos(q1_sing + sq2)
    y2 = y1 + L2 * np.sin(q1_sing + sq2)
    
    ax2.plot([x0, x1, x2], [y0, y1, y2], 'o-', color=color, linewidth=3, markersize=8, label=etiqueta)

ax2.set_xlabel("X [m]")
ax2.set_ylabel("Y [m]")
ax2.set_title("Posturas Singulares en el Espacio")
ax2.axis("equal")
ax2.grid(True, linestyle="--", alpha=0.7)
ax2.legend()

plt.tight_layout()
plt.show()