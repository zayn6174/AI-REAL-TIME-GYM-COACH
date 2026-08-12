from core.base_exercise import BaseExercise


class PlankDetector(BaseExercise):
    GOOD_ANGLE_MIN = 160
    GOOD_ANGLE_MAX = 180
    MIN_VISIBILITY = 0.7

    LEFT_SHOULDER = 11
    LEFT_HIP = 23
    LEFT_ANKLE = 27

    RIGHT_SHOULDER = 12
    RIGHT_HIP = 24
    RIGHT_ANKLE = 28

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
            ankle_idx = self.LEFT_ANKLE
        else:
            shoulder_idx = self.RIGHT_SHOULDER
            hip_idx = self.RIGHT_HIP
            ankle_idx = self.RIGHT_ANKLE

        body_angle = self.calculate_angle(
            self.get_point(landmarks, shoulder_idx),
            self.get_point(landmarks, hip_idx),
            self.get_point(landmarks, ankle_idx),
        )

        key_landmarks_visible = (
            landmarks[shoulder_idx].visibility > self.MIN_VISIBILITY
            and landmarks[hip_idx].visibility > self.MIN_VISIBILITY
            and landmarks[ankle_idx].visibility > self.MIN_VISIBILITY
        )

        if key_landmarks_visible:
            self.stage = "hold"

        if self.stage == "hold":
            if self.GOOD_ANGLE_MIN <= body_angle <= self.GOOD_ANGLE_MAX:
                form_status = "GOOD FORM"
            elif body_angle < self.GOOD_ANGLE_MIN:
                form_status = "HIPS TOO LOW"
            else:
                form_status = "HIPS TOO HIGH"
        else:
            form_status = "NOT DETECTED"

        return {
            "reps": self.reps,
            "body_angle": int(body_angle),
            "form_status": form_status,
        }