import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.animation as animation

def load_reflectivity(time_str, folder="reflectivity_pic"):
    """
    time_str: "20260424_1500"
    return: np.ndarray (881, 921)
    """

    filename = os.path.join(folder, f"{time_str}.npy")

    if not os.path.exists(filename):
        raise FileNotFoundError(f"找不到檔案: {filename}")

    grid = np.load(filename)

    return grid.astype(np.float32)

def generateTime(fromDate, fromTime, toDate, toTime):
    start = datetime.strptime(f"{fromDate}{fromTime}", "%Y%m%d%H%M")
    end = datetime.strptime(f"{toDate}{toTime}", "%Y%m%d%H%M")

    count = int((end - start).total_seconds() // 600) + 1

    return [
        (start + timedelta(minutes=10*i)).strftime("%Y%m%d_%H%M")
        for i in range(count)
    ]

time_list = generateTime("20260424", "1500", "20260424", "1650")
grid_list = []
for t in time_list:
    try:
        grid_list.append(load_reflectivity(t))
    except Exception:
        pass

# grid = load_reflectivity("20260424_1500")
# plt.imshow(grid, origin="lower", cmap="jet", vmin=0, vmax=60)
# plt.colorbar()

fig, ax = plt.subplots()

im = ax.imshow(grid_list[0], origin="lower", cmap="jet", vmin=0, vmax=60)
plt.colorbar(im)

def update(frame):
    im.set_data(grid_list[frame])
    ax.set_title(f"Time {time_list[frame]}")
    return [im]

ani = animation.FuncAnimation(
    fig,
    update,
    frames=len(grid_list),
    interval=600,   # 毫秒，越小越快
    repeat=True
)
plt.show()