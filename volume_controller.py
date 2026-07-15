import cv2
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from modules.hand_detector import HandDetector


class VolumeController:

    def __init__(self):

        self.detector = HandDetector(maxHands=1)

        # Get Speaker Device
        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

        self.minVol, self.maxVol, _ = self.volume.GetVolumeRange()

    def run(self, img):

        img = self.detector.findHands(img, draw=True)

        lmList = self.detector.findPosition(img)

        if len(lmList) != 0:

            # Thumb Tip & Index Tip Distance
            length, img = self.detector.findDistance(
                4,
                8,
                lmList,
                img,
                draw=True
            )

            # Map Finger Distance to System Volume
            volume = np.interp(
                length,
                [30, 220],
                [self.minVol, self.maxVol]
            )

            self.volume.SetMasterVolumeLevel(volume, None)

            # Volume Bar
            volume_bar = np.interp(
                length,
                [30, 220],
                [400, 150]
            )

            # Volume Percentage
            volume_percent = np.interp(
                length,
                [30, 220],
                [0, 100]
            )

            # Draw Volume Bar Outline
            cv2.rectangle(
                img,
                (50, 150),
                (85, 400),
                (255, 255, 255),
                3
            )

            # Filled Volume Bar
            cv2.rectangle(
                img,
                (50, int(volume_bar)),
                (85, 400),
                (0, 255, 0),
                cv2.FILLED
            )

            # Volume Percentage
            cv2.putText(
                img,
                f"{int(volume_percent)}%",
                (35, 440),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

        # Title
        cv2.putText(
            img,
            "Volume Controller",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        return img