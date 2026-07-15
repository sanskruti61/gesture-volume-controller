import cv2
import pyautogui
import numpy as np
import time

from modules.hand_detector import HandDetector


class VirtualMouse:

    def __init__(self):

        self.detector = HandDetector(maxHands=1)

        # Screen Size
        self.screen_width, self.screen_height = pyautogui.size()

        # Webcam Active Area
        self.frame_reduction = 100

        # Cursor Smoothening
        self.smoothening = 7

        # Previous Mouse Position
        self.prev_x = 0
        self.prev_y = 0

        self.curr_x = 0
        self.curr_y = 0

        # Gesture Settings
        self.click_threshold = 35
        self.dragging = False

        self.last_click = 0
        self.click_delay = 0.35

    def run(self, img):

        img = self.detector.findHands(img, draw=True)

        lmList = self.detector.findPosition(img)

        if len(lmList) != 0:

            x1, y1 = lmList[8][1:]   # Index Finger Tip

            h, w, _ = img.shape

            # Active Area
            cv2.rectangle(
                img,
                (self.frame_reduction, self.frame_reduction),
                (w - self.frame_reduction, h - self.frame_reduction),
                (255, 0, 255),
                2,
            )

            # Convert Webcam Coordinates to Screen Coordinates
            screen_x = np.interp(
                x1,
                (self.frame_reduction, w - self.frame_reduction),
                (0, self.screen_width),
            )

            screen_y = np.interp(
                y1,
                (self.frame_reduction, h - self.frame_reduction),
                (0, self.screen_height),
            )

            # Smooth Cursor Movement
            self.curr_x = self.prev_x + (
                screen_x - self.prev_x
            ) / self.smoothening

            self.curr_y = self.prev_y + (
                screen_y - self.prev_y
            ) / self.smoothening

            # Move Cursor (same direction as your hand)
            pyautogui.moveTo(
                self.curr_x,
                self.curr_y,
            )

            self.prev_x = self.curr_x
            self.prev_y = self.curr_y

            # Draw Index Finger
            cv2.circle(img, (x1, y1), 12, (0, 255, 0), cv2.FILLED)

            current_time = time.time()

            # ================= LEFT CLICK =================
            distance, img = self.detector.findDistance(
                4, 8, lmList, img, draw=True
            )

            if (
                distance < self.click_threshold
                and current_time - self.last_click > self.click_delay
            ):

                pyautogui.click()

                self.last_click = current_time

                cv2.putText(
                    img,
                    "LEFT CLICK",
                    (430, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3,
                )

            # ================= RIGHT CLICK =================
            distance, img = self.detector.findDistance(
                4, 12, lmList, img
            )

            if (
                distance < self.click_threshold
                and current_time - self.last_click > self.click_delay
            ):

                pyautogui.rightClick()

                self.last_click = current_time

                cv2.putText(
                    img,
                    "RIGHT CLICK",
                    (430, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    3,
                )

            # ================= DOUBLE CLICK =================
            distance, img = self.detector.findDistance(
                4, 16, lmList, img
            )

            if (
                distance < self.click_threshold
                and current_time - self.last_click > self.click_delay
            ):

                pyautogui.doubleClick()

                self.last_click = current_time

                cv2.putText(
                    img,
                    "DOUBLE CLICK",
                    (400, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    3,
                )

            # ================= DRAG =================
            distance, img = self.detector.findDistance(
                4, 20, lmList, img
            )

            if distance < self.click_threshold:

                if not self.dragging:

                    pyautogui.mouseDown()

                    self.dragging = True

                    cv2.putText(
                        img,
                        "DRAGGING",
                        (450, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 255),
                        3,
                    )

            else:

                if self.dragging:

                    pyautogui.mouseUp()

                    self.dragging = False

        # Title
        cv2.putText(
            img,
            "Virtual Mouse",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )

        return img