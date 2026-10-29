from scipy.spatial.transform import Rotation as R

# Actividad 1: 90 grados en Z
r = R.from_euler('z', 90, degrees=True)
q = r.as_quat() # [x, y, z, w]
R_mat = r.as_matrix()
print("--- ACTIVIDAD 1 ---")
print("Cuaternión:", q)
print("Matriz:\n", R_mat)

# Actividad 2: No conmutatividad
r1 = R.from_euler('z', 90, degrees=True)
r2 = R.from_euler('x', 90, degrees=True)
r_total_1 = r1 * r2
r_total_2 = r2 * r1
print("\n--- ACTIVIDAD 2 ---")
print("R1 * R2:\n", r_total_1.as_matrix())
print("R2 * R1:\n", r_total_2.as_matrix())