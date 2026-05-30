import numpy as np
import os
import tensorflow as tf

# =========================

IMG_SIZE = 128

SEQ_LEN = 6

# =========================

def load_radar(path):

    x = np.load(path)

    x = x.astype(np.float32)

    x[x == -999] = 0

    x[x == -99] = 0

    return x

# =========================

def normalize(x):

    return x / 70.0

# =========================

def resize(x):

    x = tf.image.resize(
        x[..., np.newaxis],
        (IMG_SIZE, IMG_SIZE)
    )

    return x.numpy().squeeze()

# =========================

def get_preprocess_data():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    folder = os.path.abspath(
        os.path.join(
            BASE_DIR,
            "../crawler/radar_data"
        )
    )

    files = sorted(os.listdir(folder))

    data = []

    for f in files:

        if not f.endswith(".npy"):
            continue

        path = os.path.join(folder, f)

        x = load_radar(path)

        x = normalize(x)

        x = resize(x)

        data.append(x)

    data = np.array(data)

    X = []

    y = []

    for i in range(len(data) - SEQ_LEN):

        X.append(data[i:i+SEQ_LEN])

        y.append(data[i+SEQ_LEN])

    X = np.array(X)[..., np.newaxis]

    y = np.array(y)[..., np.newaxis]

    print("X:", X.shape)

    print("y:", y.shape)

    return X, y