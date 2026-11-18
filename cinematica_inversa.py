import numpy as np
import matplotlib.pyplot as plt

# Parámetros del manipulador
L1 = 0.6
L2 = 0.4

# Puntos objetivo (Actividades 2.1 y 2.2)
puntos = {
    'A': (0.5, 0.5),
    'B': (0.95, 0.10),
    'C': (1.20, 0.20)
}

# Configuración de la figura para la Actividad 2.1 (solo punto A)
plt.figure(figsize=(8, 8))
colores_soluciones = ['#1f77b4', '#ff7f0e'] # Azul y Naranja

print("--- PARTE 2: CINEMÁTICA INVERSA ---")

for nombre, (xd, yd) in puntos.items():
    print(f"\nEvaluando Punto {nombre}: (X={xd}m, Y={yd}m)")
    
    # Cálculo del coseno de q2
    c2 = (xd**2 + yd**2 - L1**2 - L2**2) / (2 * L1 * L2)
    
    if abs(c2) > 1:
        print("  -> RESULTADO: Posición NO alcanzable (Fuera del espacio de trabajo)")
    else:
        print("  -> RESULTADO: Posición ALCANZABLE")
        # Soluciones de la segunda articulación
        q2_a = np.arccos(c2)
        q2_b = -np.arccos(c2)
        
        soluciones = []
        for q2 in [q2_a, q2_b]:
            q1 = np.arctan2(yd, xd) - np.arctan2(L2 * np.sin(q2), L1 + L2 * np.cos(q2))
            soluciones.append([q1, q2])
            
        # Verificación mediante cinemática directa y cálculo de error
        for i, (q1, q2) in enumerate(soluciones):
            x = L1 * np.cos(q1) + L2 * np.cos(q1 + q2)
            y = L1 * np.sin(q1) + L2 * np.sin(q1 + q2)
            
            error = np.hypot(xd - x, yd - y)
            print(f"  Solución {i+1}:")
            print(f"    Articulaciones [°]: q1 = {np.rad2deg(q1):.2f}°, q2 = {np.rad2deg(q2):.2f}°")
            print(f"    Posición verificada: ({x:.4f}, {y:.4f})")
            print(f"    Error (ep): {error:.4e} m")
            
            # Graficar solo las configuraciones del punto A (Actividad 2.1)
            if nombre == 'A':
                x0, y0 = 0.0, 0.0
                x1 = L1 * np.cos(q1)
                y1 = L1 * np.sin(q1)
                x2 = x1 + L2 * np.cos(q1 + q2)
                y2 = y1 + L2 * np.sin(q1 + q2)
                
                etiqueta = "Codo Abajo" if q2 > 0 else "Codo Arriba"
                plt.plot([x0, x1, x2], [y0, y1, y2], 'o-', color=colores_soluciones[i], 
                         linewidth=3, markersize=8, label=f'Solución {i+1} ({etiqueta})')

# Trazar el objetivo A en la gráfica
plt.plot(puntos['A'][0], puntos['A'][1], 'rx', markersize=12, markeredgewidth=3, label="Punto Objetivo A (0.5, 0.5)")

# Configuraciones de la gráfica
plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.title("Actividad 2.1: Múltiples soluciones de Cinemática Inversa")
plt.grid(True, linestyle="--", alpha=0.7)
plt.axis("equal")
plt.xlim(-0.2, 1.2)
plt.ylim(-0.2, 1.2)
plt.legend()
plt.show()