from scipy.spatial.transform import Rotation as R, Slerp
import numpy as np

r1 = R.from_euler('z', 0, degrees=True)
r2 = R.from_euler('z', 90, degrees=True)
slerp = Slerp([0, 1], R.concatenate([r1, r2]))

times = np.linspace(0, 1, 5)
interp = slerp(times)
print(interp.as_euler('xyz', degrees=True))