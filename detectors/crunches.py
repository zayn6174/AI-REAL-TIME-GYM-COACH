from core.base_exercise import BaseExercise


class CrunchesDetector(BaseExercise):
    UP_THRESHOLD = 60
    DOWN_THRESHOLD = 120
    MIN_VISIBILITY = 0.7

    LEFT_SHOULDER = 11
    LEFT_HIP = 23
    LEFT_KNEE = 25
    RIGHT_SHOULDER = 12
    RIGHT_HIP = 24
    RIGHT_KNEE = 26

    def __init__(self):
        super().__init__()

    def reset(self) -> None:
        self.reps = 0
        self.stage = None

    def process(self, landmarks) -> dict:
        left_vis = landmarks[self.LEFT_SHOULDER].visibility
        right_vis = landmarks[self.RIGHT_SHOULDER].visibility

        if left_vis >= right_vis:
            shoulder_idx = self.LEFT_SHOULDER
            hip_idx = self.LEFT_HIP
            knee_idx = self.LEFT_KNEE
        else:
            shoulder_idx = self.RIGHT_SHOULDER
            hip_idx = self.RIGHT_HIP
            knee_idx = self.RIGHT_KNEE

        torso_angle = self.calculate_angle(
            self.get_point(landmarks, shoulder_idx),
            self.get_point(landmarks, hip_idx),
            self.get_point(landmarks, knee_idx),
        )

        key_landmarks_visible = (
            landmarks[shoulder_idx].visibility > self.MIN_VISIBILITY
            and landmarks[hip_idx].visibility > self.MIN_VISIBILITY
            and landmarks[knee_idx].visibility > self.MIN_VISIBILITY
        )

        if key_landmarks_visible:
            if torso_angle < self.UP_THRESHOLD:
                self.stage = "up"

            if torso_angle > self.DOWN_THRESHOLD and self.stage == "up":
                self.stage = "down"
                self.reps += 1

        if torso_angle <= self.UP_THRESHOLD:
            crunch_status = "FULL CRUNCH"
        elif torso_angle <= 90:
            crunch_status = "GOOD"
        elif torso_angle <= self.DOWN_THRESHOLD:
            crunch_status = "PARTIAL"
        else:
            crunch_status = "START POSITION"

        return {
            "reps": self.reps,
            "torso_angle": int(torso_angle),
            "crunch_status": crunch_status,
        }