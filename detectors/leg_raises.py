from core.base_exercise import BaseExercise


class LegRaisesDetector(BaseExercise):
    UP_THRESHOLD = 70
    DOWN_THRESHOLD = 150
    MIN_VISIBILITY = 0.7

    LEFT_HIP = 23
    LEFT_KNEE = 25
    LEFT_ANKLE = 27

    RIGHT_HIP = 24
    RIGHT_KNEE = 26
    RIGHT_ANKLE = 28

    def __init__(self):
        super().__init__()

    def reset(self) -> None:
        self.reps = 0
        self.stage = None

    def process(self, landmarks) -> dict:
        left_vis = landmarks[self.LEFT_ANKLE].visibility
        right_vis = landmarks[self.RIGHT_ANKLE].visibility

        if left_vis >= right_vis:
            hip_idx = self.LEFT_HIP
            knee_idx = self.LEFT_KNEE
            ankle_idx = self.LEFT_ANKLE
        else:
            hip_idx = self.RIGHT_HIP
            knee_idx = self.RIGHT_KNEE
            ankle_idx = self.RIGHT_ANKLE

        hip_angle = self.calculate_angle(
            self.get_point(landmarks, knee_idx),
            self.get_point(landmarks, hip_idx),
            self.get_point(landmarks, ankle_idx),
        )

        knee_angle = self.calculate_angle(
            self.get_point(landmarks, hip_idx),
            self.get_point(landmarks, knee_idx),
            self.get_point(landmarks, ankle_idx),
        )

        key_landmarks_visible = (
            landmarks[hip_idx].visibility > self.MIN_VISIBILITY
            and landmarks[knee_idx].visibility > self.MIN_VISIBILITY
            and landmarks[ankle_idx].visibility > self.MIN_VISIBILITY
        )

        if key_landmarks_visible:
            if hip_angle < self.UP_THRESHOLD:
                self.stage = "up"

            if hip_angle > self.DOWN_THRESHOLD and self.stage == "up":
                self.stage = "down"
                self.reps += 1

        if hip_angle <= self.UP_THRESHOLD:
            movement_status = "LEGS UP"
        elif hip_angle <= 100:
            movement_status = "GOOD"
        elif hip_angle <= self.DOWN_THRESHOLD:
            movement_status = "PARTIAL"
        else:
            movement_status = "START POSITION"

        if knee_angle >= 160:
            leg_status = "LEGS STRAIGHT"
        elif knee_angle >= 120:
            leg_status = "GOOD"
        else:
            leg_status = "BEND YOUR KNEES"

        return {
            "reps": self.reps,
            "hip_angle": int(hip_angle),
            "knee_angle": int(knee_angle),
            "movement_status": movement_status,
            "leg_status": leg_status,
        }