import math

class SpeedCalculator:

    def __init__(self, scale, fps):
        self.scale = scale
        self.fps = fps

    def calculate(self, prev, curr):
        dist_px = math.hypot(curr[0]-prev[0], curr[1]-prev[1])

        # 🚨 FILTRO DE SALTO IRREAL
        if dist_px > 80:
            return 0

        dist_m = dist_px * self.scale
        return dist_m * self.fps * 3.6