from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import ConvLSTM2D, BatchNormalization, Conv2D
import tensorflow as tf

from preprocess import get_preprocess_data
from keras.saving import register_keras_serializable


@register_keras_serializable()
def weighted_mae(y_true, y_pred):
    weight = 1 + 5 * y_true
    return tf.reduce_mean(weight * tf.abs(y_true - y_pred))


X, y = get_preprocess_data()

model = Sequential()

model.add(
    ConvLSTM2D(
        filters=32,
        kernel_size=(3, 3),
        input_shape=(6, 256, 256, 1),
        padding="same",
        return_sequences=False,
    )
)

model.add(BatchNormalization())

model.add(Conv2D(filters=1, kernel_size=(3, 3), activation="linear", padding="same"))


def weighted_mae(y_true, y_pred):
    weight = 1 + 5 * y_true  # 雨越大權重越高
    return tf.reduce_mean(weight * tf.abs(y_true - y_pred))


model.compile(optimizer="adam", loss=weighted_mae)

model.fit(X, y, batch_size=2, epochs=20, validation_split=0.1)

model.save("model.keras")
