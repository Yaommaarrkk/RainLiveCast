import numpy as np
import os
import tensorflow as tf

def load_radar(path):
    x = np.load(path)

    # 無效值處理
    x[x == -999] = 0
    x[x == -99] = 0

    return x

def normalize(x):
    return x / 70.0

def resize(x):
    x = tf.image.resize(x[..., np.newaxis], (256, 256))
    return x.numpy().squeeze()

def get_preprocess_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(BASE_DIR, "reflectivity_pic")
    files = sorted(os.listdir(folder))

    data = []

    for f in files:
        x = load_radar(folder + "/" + f)
        x = normalize(x)
        x = resize(x)
        data.append(x)

    data = np.array(data)

    seq_len = 6

    X = []
    y = []

    for i in range(len(data) - seq_len):
        X.append(data[i:i+seq_len])
        y.append(data[i+seq_len])

    X = np.array(X)
    y = np.array(y)

    # 加channel
    X = X[..., np.newaxis]
    y = y[..., np.newaxis]

    # print(X.shape, y.shape)
    return X, y