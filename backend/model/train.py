from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import ConvLSTM2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D

import tensorflow as tf

from backend.preprocess.preprocess import get_preprocess_data

from keras.saving import register_keras_serializable

# =========================

MODEL_PATH = "backend/model/model.keras"

# =========================

@register_keras_serializable()
def weighted_mae(y_true, y_pred):

    weight = 1 + 5 * y_true

    return tf.reduce_mean(
        weight * tf.abs(y_true - y_pred)
    )

# =========================

print("============================")
print("讀取資料")
print("============================")

X, y = get_preprocess_data()

print("============================")
print("建立模型")
print("============================")

model = Sequential()

model.add(
    ConvLSTM2D(
        filters=8,
        kernel_size=(3, 3),
        input_shape=(6, 128, 128, 1),
        padding="same",
        return_sequences=False
    )
)

model.add(BatchNormalization())

model.add(
    Conv2D(
        filters=1,
        kernel_size=(3, 3),
        activation="linear",
        padding="same"
    )
)

model.compile(
    optimizer="adam",
    loss=weighted_mae
)

print("============================")
print("開始訓練")
print("============================")

model.fit(
    X,
    y,
    batch_size=2,
    epochs=5,
    validation_split=0.1
)

print("============================")
print("儲存模型")
print("============================")

model.save(MODEL_PATH)

print("模型已儲存:", MODEL_PATH)