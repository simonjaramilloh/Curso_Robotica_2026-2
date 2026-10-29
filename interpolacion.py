from scipy.spatial.transform import Rotation as R, Slerp
import numpy as np

key_times = [0, 1]
rots = R.from_euler('z', [0, 90], degrees=True)
slerp = Slerp(key_times, rots)
times = np.linspace(0, 1, 5)
interp = slerp(times)
print("Interpolación en grados:\n", interp.as_euler('xyz', degrees=True))