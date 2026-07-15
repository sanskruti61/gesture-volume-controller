import cv2
import numpy as np
import screen_brightness_control as sbc

from modules.hand_detector import HandDetector


class BrightnessController:

    def __init__(self):

        self.detector = HandDetector(maxHands=1)

    def run(self, img):

        img = self.detector.findHands(img, draw=True)

        lmList = self.detector.findPosition(img)

        if len(lmList) != 0:

            length, img = self.detector.findDistance(
                4,
                8,
                lmList,
                img,
                draw=True
            )

            brightness = np.interp(
                length,
                [30, 220],
                [0, 100]
            )

            sbc.set_brightness(int(brightness))

            brightness_bar = np.interp(
                brightness,
                [0, 100],
                [400, 150]
            )

            cv2.rectangle(
                img,
                (50, 150),
                (85, 400),
                (255, 255, 255),
                3
            )

            cv2.rectangle(
                img,
                (50, int(brightness_bar)),
                (85, 400),
                (0, 255, 255),
                cv2.FILLED
            )

            cv2.putText(
                img,
                f"{int(brightness)}%",
                (25, 440),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

        cv2.putText(
            img,
            "Brightness Controller",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        return img