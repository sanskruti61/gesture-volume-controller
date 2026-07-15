import cv2
import numpy as np


def load_png(path, size=None):

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise FileNotFoundError(path)

    if size is not None:
        img = cv2.resize(img, size)

    return img


def overlay(background, overlay, x, y):

    h, w = overlay.shape[:2]

    if overlay.shape[2] == 4:

        alpha = overlay[:, :, 3] / 255.0

        for c in range(3):
            background[y:y+h, x:x+w, c] = (
                alpha * overlay[:, :, c] +
                (1 - alpha) * background[y:y+h, x:x+w, c]
            )

    else:

        background[y:y+h, x:x+w] = overlay

    return background