import math
from config import BALL_CLASS_ID, MAX_PRED_FRAMES, SMOOTH_ALPHA

class BallTracker:

    def __init__(self, model):
        self.model = model
        self.prev_center = None
        self.prev_box = None
        self.dx, self.dy = 0, 0
        self.lost_frames = 0

    def center(self, box):
        x1, y1, x2, y2 = box
        return (int((x1+x2)/2), int((y1+y2)/2))

    def smooth(self, prev, curr):
        alpha = 0.7
        return (
            int(alpha*prev[0] + (1-alpha)*curr[0]),
            int(alpha*prev[1] + (1-alpha)*curr[1])
        )

    def detect(self, frame):
        results = self.model.predict(frame, imgsz=640, conf=0.25, verbose=False)

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes:
                if int(box.cls[0]) == BALL_CLASS_ID:
                    return tuple(map(int, box.xyxy[0]))

        return None

    def update(self, frame):
        h, w, _ = frame.shape
        margin = 200

        if self.prev_center:
            cx, cy = self.prev_center

            x1 = max(0, cx - margin)
            y1 = max(0, cy - margin)
            x2 = min(w, cx + margin)
            y2 = min(h, cy + margin)

            roi = frame[y1:y2, x1:x2]
        else:
            roi = frame
            x1, y1 = 0, 0

        box = self.detect(roi)

        if box is not None:
            box = (box[0]+x1, box[1]+y1, box[2]+x1, box[3]+y1)
            center = self.center(box)

            if self.prev_center:
                self.dx = center[0] - self.prev_center[0]
                self.dy = center[1] - self.prev_center[1]
                center = self.smooth(self.prev_center, center)

            self.lost_frames = 0

        else:
            self.lost_frames += 1

            if self.lost_frames < 5 and self.prev_center:
                center = (
                    int(self.prev_center[0] + self.dx),
                    int(self.prev_center[1] + self.dy)
                )
                box = (center[0]-5, center[1]-5, center[0]+5, center[1]+5)
            else:
                return None, None

        return center, box