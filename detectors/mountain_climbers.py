from core.base_exercise import BaseExercise


class MountainClimbersDetector(BaseExercise):
    KNEE_UP_THRESHOLD = 100
    KNEE_DOWN_THRESHOLD = 150
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
        left_knee_angle = self.calculate_angle(
            self.get_point(landmarks, self.LEFT_SHOULDER),
            self.get_point(landmarks, self.LEFT_HIP),
            self.get_point(landmarks, self.LEFT_KNEE),
        )

        right_knee_angle = self.calculate_angle(
            self.get_point(landmarks, self.RIGHT_SHOULDER),
            self.get_point(landmarks, self.RIGHT_HIP),
            self.get_point(landmarks, self.RIGHT_KNEE),
        )

        key_landmarks_visible = (
            landmarks[self.LEFT_SHOULDER].visibility > self.MIN_VISIBILITY
            and landmarks[self.LEFT_HIP].visibility > self.MIN_VISIBILITY
            and landmarks[self.LEFT_KNEE].visibility > self.MIN_VISIBILITY
            and landmarks[self.RIGHT_SHOULDER].visibility > self.MIN_VISIBILITY
            and landmarks[self.RIGHT_HIP].visibility > self.MIN_VISIBILITY
            and landmarks[self.RIGHT_KNEE].visibility > self.MIN_VISIBILITY
        )

        if key_landmarks_visible:

            if left_knee_angle < self.KNEE_UP_THRESHOLD:
                if self.stage == "right_up":
                    self.reps += 1

                self.stage = "left_up"

            elif right_knee_angle < self.KNEE_UP_THRESHOLD:
                if self.stage == "left_up":
                    self.reps += 1

                self.stage = "right_up"

            elif (
                left_knee_angle > self.KNEE_DOWN_THRESHOLD
                and right_knee_angle > self.KNEE_DOWN_THRESHOLD
            ):
                self.stage = "down"

        if left_knee_angle < self.KNEE_UP_THRESHOLD:
            left_knee_status = "KNEE UP"
        elif left_knee_angle < self.KNEE_DOWN_THRESHOLD:
            left_knee_status = "MOVING"
        else:
            left_knee_status = "KNEE DOWN"

        if right_knee_angle < self.KNEE_UP_THRESHOLD:
            right_knee_status = "KNEE UP"
        elif right_knee_angle < self.KNEE_DOWN_THRESHOLD:
            right_knee_status = "MOVING"
        else:
            right_knee_status = "KNEE DOWN"

        return {
            "reps": self.reps,
            "left_knee_angle": int(left_knee_angle),
            "right_knee_angle": int(right_knee_angle),
            "left_knee_status": left_knee_status,
            "right_knee_status": right_knee_status,
        }