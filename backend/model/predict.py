import os
import cv2
import numpy as np
import tensorflow as tf

from tensorflow.keras.models import load_model
from keras.saving import register_keras_serializable

MODEL_PATH = "backend/model/model.keras"

DATA_FOLDER = "backend/crawler/radar_data"

IMG_SIZE = 128
SEQ_LEN = 6
DBZ_MAX = 70.0

# =========================

@register_keras_serializable()
def weighted_mae(y_true, y_pred):

    weight = 1 + 5 * y_true

    return tf.reduce_mean(
        weight * tf.abs(y_true - y_pred)
    )

# =========================

model = None

def get_model():

    global model

    if model is None:

        print("載入模型...")

        model = load_model(
            MODEL_PATH,
            compile=False
        )

        print("模型載入完成")

    return model

# =========================

def load_npy(path):

    x = np.load(path)

    # 避免 object array
    if x.dtype == object:
        raise Exception(f"壞檔案(object): {path}")

    x = x.astype(np.float32)

    # shape檢查
    if len(x.shape) != 2:
        raise Exception(f"shape錯誤: {path}")

    # normalize
    x = x / DBZ_MAX

    return x

# =========================

def predict_future():

    try:

        model = get_model()

        files = sorted([
            f for f in os.listdir(DATA_FOLDER)
            if f.endswith(".npy")
        ])

        print("找到檔案數:", len(files))

        seq = []

        for f in reversed(files):

            try:

                path = os.path.join(
                    DATA_FOLDER,
                    f
                )

                img = load_npy(path)

                img = cv2.resize(
                    img,
                    (IMG_SIZE, IMG_SIZE)
                )

                seq.append(img)

                print("成功讀取:", f)

                if len(seq) >= SEQ_LEN:
                    break

            except Exception as e:

                print("跳過壞檔:", f)
                print(e)

        if len(seq) < SEQ_LEN:

            return {
                "error": "有效雷達資料不足"
            }

        seq.reverse()

        x = np.array(seq)[..., np.newaxis]

        x = x[np.newaxis, ...]

        print("模型輸入shape:", x.shape)

        pred = model.predict(
            x,
            verbose=0
        )[0, :, :, 0]

        pred = pred * DBZ_MAX

        rain_prob = np.clip(
            pred / 60.0 * 100,
            0,
            100
        )

        return {
            "radar": pred.tolist(),
            "rain_probability": rain_prob.tolist()
        }

    except Exception as e:

        print("predict錯誤:")
        print(e)

        return {
            "error": str(e)
        }