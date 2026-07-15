import cv2
import mediapipe as mp
import math


class HandDetector:

    def __init__(
        self,
        mode=False,
        maxHands=1,
        detectionCon=0.6,
        trackCon=0.5
    ):

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

        self.mpDraw = mp.solutions.drawing_utils
        self.results = None

    def findHands(self, img, draw=False):
        """
        Detect hands in the image.

        Args:
            img: Input BGR image
            draw: Draw hand landmarks

        Returns:
            Image with optional landmarks
        """

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(imgRGB)

        if self.results and self.results.multi_hand_landmarks:

            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(
                        img,
                        handLms,
                        self.mpHands.HAND_CONNECTIONS
                    )

        return img

    def findPosition(self, img, handNo=0):
        """
        Returns landmark positions.

        Returns:
            lmList = [[id, x, y], ...]
        """

        lmList = []

        if self.results and self.results.multi_hand_landmarks:

            myHand = self.results.multi_hand_landmarks[handNo]

            h, w, _ = img.shape

            for idx, lm in enumerate(myHand.landmark):

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                lmList.append([idx, cx, cy])

        return lmList

    def findDistance(self, p1, p2, lmList, img=None, draw=False):
        """
        Calculate distance between two landmarks.

        Args:
            p1: Landmark ID 1
            p2: Landmark ID 2
            lmList: Landmark list
            img: Image (optional)
            draw: Draw line and points

        Returns:
            length, img
        """

        if len(lmList) == 0:
            return 0, img

        x1, y1 = lmList[p1][1:]
        x2, y2 = lmList[p2][1:]

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        length = math.hypot(x2 - x1, y2 - y1)

        if draw and img is not None:

            cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)

            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)

        return length, img