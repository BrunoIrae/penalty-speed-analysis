import cv2
import math
import time
from ultralytics import YOLO

from config import *
from videoProcessor import VideoProcessor
from ballTracker import BallTracker
from goalDetector import GoalDetector
from speedCalculator import SpeedCalculator


def wait_exit(seconds=5):
    """
    Espera ESC ou tempo limite (evita travamento)
    """
    start = time.time()

    while True:
        key = cv2.waitKey(1)

        if key == 27:  # ESC
            break

        if time.time() - start > seconds:
            break


def main():

    video = VideoProcessor(VIDEO_PATH)
    model = YOLO(MODEL_PATH)

    ret, frame = video.read()
    if not ret:
        return

    # =========================
    # Selecionar bola
    # =========================
    cv2.rectangle(frame, (40, 20), (600, 90), (0, 0, 0), -1)
    cv2.putText(frame, "Selecione a BOLA e pressione ENTER",
                (50, 65), cv2.FONT_HERSHEY_SIMPLEX,
                0.9, (0,255,255), 2, cv2.LINE_AA)

    bbox = cv2.selectROI("Tracking", frame, False)
    cv2.destroyAllWindows()

    tracker = BallTracker(model)
    tracker.prev_box = (int(bbox[0]), int(bbox[1]),
                        int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3]))
    tracker.prev_center = tracker.center(tracker.prev_box)

    # =========================
    # Selecionar traves
    # =========================
    points = []

    def mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < 2:
            points.append((x,y))

    cv2.imshow("Tracking", frame)
    cv2.waitKey(1)
    cv2.setMouseCallback("Tracking", mouse)

    while True:
        temp = frame.copy()

        cv2.rectangle(temp, (40, 20), (750, 80), (0, 0, 0), -1)
        cv2.putText(temp, "Clique nas DUAS TRAVES e pressione ENTER",
                    (50, 60), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0,255,255), 2, cv2.LINE_AA)

        for p in points:
            cv2.circle(temp, p, 5, (0,0,255), -1)

        cv2.imshow("Tracking", temp)

        if cv2.waitKey(1) == 13 and len(points) == 2:
            break

    left_post, right_post = points

    # =========================
    # ESCALA
    # =========================
    goal_px = math.hypot(left_post[0]-right_post[0],
                         left_post[1]-right_post[1])

    scale = (GOAL_WIDTH_METERS / goal_px) * 0.75
    print(f"[INFO] Escala: {scale:.5f}")

    goal_detector = GoalDetector(left_post, right_post)
    speed_calc = SpeedCalculator(scale, video.fps)

    speeds = []
    iniciou_chute = False
    positions = []

    # =========================
    # LOOP PRINCIPAL
    # =========================
    while True:

        ret, frame = video.read()
        if not ret:
            break

        prev_center = tracker.prev_center
        prev_box = tracker.prev_box

        center, box = tracker.update(frame)

        if center is None:
            tracker.prev_center = None
            continue

        # =========================
        # VELOCIDADE
        # =========================
        if prev_center:
            speed = speed_calc.calculate(prev_center, center)

            if speed is None:
                continue

            # DETECÇÃO DE CHUTE
            if not iniciou_chute and speed > 15:
                iniciou_chute = True
                print("🚀 CHUTE DETECTADO")

            if iniciou_chute:
                speeds.append(speed)

        # =========================
        # GOL
        # =========================
        if iniciou_chute and prev_box and box:
            if goal_detector.crossed(prev_box, box):

                print("⚽ GOL DETECTADO")

                freeze = frame.copy()

                cv2.putText(freeze, "GOL",
                            (50,150), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (0,255,0), 4)

                cv2.imshow("Tracking", freeze)

                wait_exit(5)  
                break

        # =========================
        # ATUALIZA
        # =========================
        tracker.prev_center = center
        tracker.prev_box = box
        positions.append(center)

        # =========================
        # VISUAL
        # =========================
        x1,y1,x2,y2 = box
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.circle(frame, center, 5, (0,0,255), -1)

        for i in range(1, len(positions)):
            cv2.line(frame, positions[i-1], positions[i], (255,255,0), 2)

        cv2.line(frame, left_post, right_post, (0,255,0), 2)

        if speeds:
            cv2.putText(frame, f"{speeds[-1]:.2f} km/h",
                        (50,50), cv2.FONT_HERSHEY_SIMPLEX,
                        1,(0,0,255),2)

        if iniciou_chute:
            cv2.putText(frame, "CHUTE EXECUTADO",
                        (50,100), cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,(0,255,255),3)

        cv2.imshow("Tracking", frame)

        if cv2.waitKey(1) == 27:
            break

    video.release()
    cv2.destroyAllWindows()

    # =========================
    # RESULTADO FINAL
    # =========================
    if speeds:
        max_speed = max(speeds)
        avg_speed = sum(speeds)/len(speeds)

        print(f"🔥 Vel Max: {max_speed:.2f}")
        print(f"📊 Vel Média: {avg_speed:.2f}")

        result = frame.copy()

        cv2.putText(result, "RESULTADO FINAL",
                    (50,150), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,(0,255,0),3)

        cv2.putText(result, f"MAX: {max_speed:.2f} km/h",
                    (50,200), cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,255,0),3)

        cv2.putText(result, f"MEDIA: {avg_speed:.2f} km/h",
                    (50,250), cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,255,0),3)

        cv2.imshow("RESULTADO FINAL", result)

        wait_exit(5)  


if __name__ == "__main__":
    main()