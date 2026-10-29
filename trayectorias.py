from roboticstoolbox import quintic, trapezoidal
import numpy as np

# Vector de tiempo: 50 pasos entre 0 y 1
t = np.linspace(0, 1, 50)

# Actividad 4: Trayectoria quíntica
traj_q = quintic(0, 1, t)
print("--- Trayectoria Quíntica ---")
print(traj_q.q)

# Actividad 5: Trayectoria trapezoidal
traj_t = trapezoidal(0, 1, t)
print("\n--- Trayectoria Trapezoidal ---")
print(traj_t.q)