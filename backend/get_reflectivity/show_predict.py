import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tensorflow.keras.models import load_model
import cv2
import tensorflow as tf
from keras.saving import register_keras_serializable

# =========================
# 設定
# =========================
MODEL_PATH = "model.keras"
DATA_FOLDER = "backend/get_reflectivity/reflectivity_pic"

SEQ_LEN = 6
IMG_SIZE = (256, 256)
DBZ_MAX = 70.0


@register_keras_serializable()
def weighted_mae(y_true, y_pred):
    weight = 1 + 5 * y_true
    return tf.reduce_mean(weight * tf.abs(y_true - y_pred))


def preprocess_input(seq):
    out = []

    for frame in seq:
        img = frame[:, :, 0]
        img = cv2.resize(img, (256, 256))
        out.append(img)

    out = np.array(out)[..., np.newaxis]
    return out


# =========================
# 讀資料
# =========================
def load_npy(path):
    x = np.load(path)

    x = x.astype(np.float32)

    # normalize
    x = x / DBZ_MAX

    return x


def get_sorted_files():
    files = sorted([f for f in os.listdir(DATA_FOLDER) if f.endswith(".npy")])
    return files


# =========================
# 建序列
# =========================
files = get_sorted_files()
data = []

for f in files:
    path = os.path.join(DATA_FOLDER, f)
    data.append(load_npy(path))

data = np.array(data)

X = []
y = []

for i in range(len(data) - SEQ_LEN):
    X.append(data[i : i + SEQ_LEN])
    y.append(data[i + SEQ_LEN])

X = np.array(X)[..., np.newaxis]
y = np.array(y)[..., np.newaxis]

print("X:", X.shape)
print("y:", y.shape)

# =========================
# 載入模型
# =========================
model = load_model(MODEL_PATH, compile=False)

# =========================
# 預測一段時間序列
# =========================
idx_start = 0
steps = 20

true_seq = []
pred_seq = []
for i in range(idx_start, idx_start + steps):

    x_input = preprocess_input(X[i])  # (6,256,256,1)
    x_input = x_input[np.newaxis, ...]  # (1,6,256,256,1)

    pred = model.predict(x_input, verbose=0)[0, :, :, 0]
    true = y[i, :, :, 0]

    # 還原 dBZ
    pred = pred * DBZ_MAX
    true = true * DBZ_MAX

    # ⭐ 這行才是關鍵
    pred = cv2.resize(pred, (true.shape[1], true.shape[0]))

    pred_seq.append(pred)
    true_seq.append(true)
# =========================
# 畫動畫
# =========================
fig, axs = plt.subplots(1, 3, figsize=(12, 4))


def update(frame):
    axs[0].clear()
    axs[1].clear()
    axs[2].clear()

    true = true_seq[frame]
    pred = pred_seq[frame]
    err = abs(true - pred)

    axs[0].imshow(true, origin="lower", cmap="jet", vmin=0, vmax=60)
    axs[0].set_title("True")

    axs[1].imshow(pred, origin="lower", cmap="jet", vmin=0, vmax=60)
    axs[1].set_title("Pred")

    axs[2].imshow(err, origin="lower", cmap="hot")
    axs[2].set_title("Error")


ani = animation.FuncAnimation(
    fig, update, frames=len(true_seq), interval=500, repeat=True
)

plt.show()
