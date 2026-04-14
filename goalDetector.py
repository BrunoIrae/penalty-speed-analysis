class GoalDetector:

    def __init__(self, left_post, right_post):
        self.p1 = left_post
        self.p2 = right_post

    def front_point(self, box):
        x1, y1, x2, y2 = box
        return (x1, int((y1+y2)/2))

    def crossed(self, prev_box, curr_box):
        prev_pt = self.front_point(prev_box)
        curr_pt = self.front_point(curr_box)

        x1, y1 = self.p1
        x2, y2 = self.p2

        A = y2 - y1
        B = x1 - x2
        C = x2*y1 - x1*y2

        def side(p):
            return A*p[0] + B*p[1] + C

        return side(prev_pt) * side(curr_pt) <= 0