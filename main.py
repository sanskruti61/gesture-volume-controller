import cv2

from modules.mouse_controller import VirtualMouse
from modules.volume_controller import VolumeController
from modules.brightness_controller import BrightnessController
from modules.image_loader import load_png, overlay


# ==============================
# Webcam
# ==============================

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# ==============================
# Controllers
# ==============================

mouse = VirtualMouse()
volume = VolumeController()
brightness = BrightnessController()


# ==============================
# Load Assets
# ==============================

background = load_png("assets/background.png", (1280, 720))
logo = load_png("assets/logo.png", (420, 180))

mouse_icon = load_png("assets/mouse.png", (90, 90))
volume_icon = load_png("assets/volume.png", (90, 90))
brightness_icon = load_png("assets/brightness.png", (90, 90))


# ==============================
# Current Mode
# ==============================

mode = "menu"


# ==============================
# Main Loop
# ==============================

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    if mode == "menu":

        img = background.copy()

        # Logo
        overlay(img, logo, 430, 20)

        # Icons
        overlay(img, mouse_icon, 170, 250)
        overlay(img, volume_icon, 560, 250)
        overlay(img, brightness_icon, 950, 250)

        # Mouse
        cv2.putText(
            img,
            "Press M",
            (160, 380),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            img,
            "Virtual Mouse",
            (125, 420),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        # Volume
        cv2.putText(
            img,
            "Press V",
            (550, 380),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            img,
            "Volume Controller",
            (500, 420),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        # Brightness
        cv2.putText(
            img,
            "Press L",
            (940, 380),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            img,
            "Brightness",
            (910, 420),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        # Footer
        cv2.line(img, (80, 610), (1200, 610), (0, 255, 255), 1)

        cv2.putText(
            img,
            "M - Mouse      V - Volume      L - Brightness      ESC - Exit",
            (220, 650),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            2,
        )

    elif mode == "mouse":

        img = frame.copy()

        img = mouse.run(img)

        cv2.rectangle(img, (0, 0), (1280, 60), (35, 35, 35), -1)

        cv2.putText(
            img,
            "Virtual Mouse",
            (25, 38),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            img,
            "Press B : Menu",
            (980, 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            2,
        )

    elif mode == "volume":

        img = frame.copy()

        img = volume.run(img)

        cv2.rectangle(img, (0, 0), (1280, 60), (35, 35, 35), -1)

        cv2.putText(
            img,
            "Volume Controller",
            (25, 38),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            img,
            "Press B : Menu",
            (980, 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            2,
        )

    elif mode == "brightness":

        img = frame.copy()

        img = brightness.run(img)

        cv2.rectangle(img, (0, 0), (1280, 60), (35, 35, 35), -1)

        cv2.putText(
            img,
            "Brightness Controller",
            (25, 38),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            img,
            "Press B : Menu",
            (980, 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            2,
        )

    cv2.imshow("AI Gesture Control Suite", img)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        mode = "mouse"

    elif key == ord("v"):
        mode = "volume"

    elif key == ord("l"):
        mode = "brightness"

    elif key == ord("b"):
        mode = "menu"

    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()