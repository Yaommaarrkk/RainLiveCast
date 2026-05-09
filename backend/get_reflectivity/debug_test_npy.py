import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

path = os.path.join(BASE_DIR, "reflectivity_pic", "20260503_0010.npy")

x = np.load(path, allow_pickle=True)

print(type(x), x.dtype)

if isinstance(x, np.ndarray):
    print("shape:", x.shape)

    if x.dtype == object:
        print("⚠️ 這是 object（壞檔案）")
        print("內容型態:", type(x.item()))
    else:
        print("✔ 正常數值陣列")

folder = "backend/get_reflectivity/reflectivity_pic"

for f in os.listdir(folder):
    path = os.path.join(folder, f)
    
    x = np.load(path, allow_pickle=True)

    if x.dtype != np.float32 or x.shape != (881, 921):
        print("壞檔:", f, x.dtype, x.shape)