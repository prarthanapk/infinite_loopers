import cv2
import mediapipe as mp
import pyautogui
import subprocess
import webbrowser
import time
import os
import pygame

# Initialize
pygame.mixer.init()
clap_sound = pygame.mixer.Sound(os.path.join("sounds", "clap_sound.mp3"))

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

def get_gesture(lm_list):
    fingers = [1 if lm_list[4][0] > lm_list[3][0] else 0]
    for tip in [8, 12, 16, 20]:
        fingers.append(1 if lm_list[tip][1] < lm_list[tip - 2][1] else 0)

    if fingers == [0, 1, 1, 0, 0]:
        return "peace"
    elif fingers == [0, 0, 0, 0, 0]:
        return "fist"
    elif fingers == [1, 1, 1, 1, 1]:
        return "open"
    elif fingers == [0, 1, 1, 1, 1]:
        return "wave"
    elif fingers == [1, 1, 0, 0, 1]:
        return "clap"
    elif fingers == [1, 0, 0, 0, 1]:
        return "rock"
    return "unknown"

def perform_action(gesture):
    if gesture == "open":
        print("Detected ✋ Open Palm")
        subprocess.Popen(['notepad.exe'])
        time.sleep(1)
        for _ in range(5):
            pyautogui.typewrite("I'm wasting time\n")
            time.sleep(0.5)

    elif gesture == "peace":
        print("Detected ✌️ Peace")
        pyautogui.hotkey('win', 'd')
        time.sleep(1)
        subprocess.Popen(['mspaint.exe'])

    elif gesture == "fist":
        print("Detected 👊 Fist")
        screenshot = pyautogui.screenshot()
        screenshot.save("temp_screenshot.png")
        os.remove("temp_screenshot.png")
        print("Screenshot taken and deleted.")

    elif gesture == "wave":
        print("Detected 🤚 Wave — Playing video!")

        video_path = os.path.join("videos", "wave_video.mp4")
        if os.path.exists(video_path):
            cap_video = cv2.VideoCapture(video_path)

            while cap_video.isOpened():
                ret, frame = cap_video.read()
                if not ret:
                    break  # Video finished

                cv2.imshow("👋 Waving Video", frame)
                if cv2.waitKey(25) & 0xFF == 27:  # ESC to stop
                    break

            cap_video.release()
            cv2.destroyWindow("👋 Waving Video")
        else:
            print("⚠️ 'wave_video.mp4' not found in videos/ folder.")

    elif gesture == "clap":
        print("👐 Clap Detected — Opening YouTube")
        for _ in range(10):
            webbrowser.open_new_tab("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            time.sleep(0.5)

    elif gesture == "rock":
        print("🤙 Rock sign detected — Playing clap sound")
        clap_sound.play()

# Webcam loop
cap = cv2.VideoCapture(0)  # Change to 1 if external webcam

while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    lm_list = []
    if result.multi_hand_landmarks:
        for hand_landmark in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS)
            h, w, _ = img.shape
            for lm in hand_landmark.landmark:
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

        if lm_list:
            gesture = get_gesture(lm_list)
            if gesture != "unknown":
                perform_action(gesture)
                time.sleep(5)

    cv2.imshow("Hand Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
