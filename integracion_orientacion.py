from scipy.spatial.transform import Rotation as R
import numpy as np

dt = 0.01
w = np.array([0, 0, 1])
r = R.identity()

for i in range(100):
    r = r * R.from_rotvec(w * dt)

print(r.as_euler('xyz', degrees=True))
