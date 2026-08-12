import time
import streamlit as st


class VoicePipeline:
    def __init__(self, llm, tts):
        self.llm = llm
        self.tts = tts
        self.last_spoken_at = 0

    def _find_form_issue(self, exercise, metrics):
        if "issue" in metrics:
            return metrics["issue"]

        if exercise == "Squats":
            depth = metrics.get("depth_status", "")
            back_angle = metrics.get("back_angle", 180)
            
            if depth == "TOO HIGH":
                return "The user's squat is not deep enough — knees are not bending sufficiently."

            if isinstance(back_angle, (int, float)) and back_angle < 130:
                return "The user is leaning too far forward during the squat."

        elif exercise == "Push-ups":
            alignment = metrics.get("body_alignment", "")
            hip_status = metrics.get("hip_status", "")
            
            if alignment == "Poor Form":
                return "The user's body is not straight during the push-up."

            if hip_status == "SAGGING":
                return "The user's hips are sagging down during the push-up."

            if hip_status == "PIKED UP":
                return "The user's hips are too high — lower them to form a straight line."

        elif exercise == "Dumbbell Bicep Curls":
            swing = metrics.get("swing_status", "")
            shoulder = metrics.get("shoulder_status", "")
            
            if swing == "SWINGING":
                return "The user is swinging their torso during the curl — keep the body still."

            if shoulder == "ELBOW DRIFTING":
                return "The user's elbow is drifting away from their side during the curl."

        elif exercise == "Shoulder Press":
            back_arch = metrics.get("back_arch_status", "")
            extension = metrics.get("extension_status", "")
            
            if back_arch == "Excessive Arch":
                return "The user is arching their lower back excessively during the press."

            if back_arch == "Slight Arch":
                return "Slight back arch detected — encourage the user to brace their core."

        elif exercise == "Lunges":
            balance = metrics.get("balance_status", "")
            
            if balance == "OFF BALANCE":
                return "The user is losing balance during the lunge — feet should be hip-width apart."


        elif exercise == "Leg Press":
            depth = metrics.get("depth_status", "")
            
            if depth == "TOO HIGH":
                return "The user's leg press is not deep enough — knees should bend sufficiently before pressing back up."

        elif exercise == "Crunches":
            crunch_status = metrics.get("crunch_status", "")
            
            if crunch_status == "PARTIAL":
                return "The user is not completing the crunch fully — encourage a greater range of motion."

            if crunch_status == "START POSITION":
                return "The user has not started the crunch movement yet."

        elif exercise == "Reverse Crunches":
            movement_status = metrics.get("movement_status", "")
            leg_status = metrics.get("leg_status", "")
            
            if movement_status == "PARTIAL":
                return "The user's reverse crunch is incomplete — encourage a fuller contraction."

            if leg_status == "LEGS STRAIGHT":
                return "The user's legs are too straight during the reverse crunch — keep the knees slightly bent."

        elif exercise == "Leg Raises":
            movement_status = metrics.get("movement_status", "")
            leg_status = metrics.get("leg_status", "")
            
            if movement_status == "PARTIAL":
                return "The user's leg raise is incomplete — raise the legs through a greater range of motion."

            if leg_status == "BEND YOUR KNEES":
                return "The user's knees are bending during the leg raise — keep the legs as straight as possible."

        elif exercise == "Mountain Climbers":
            left_knee_status = metrics.get("left_knee_status", "")
            right_knee_status = metrics.get("right_knee_status", "")
            
            if left_knee_status == "MOVING" or right_knee_status == "MOVING":
                return "The user needs to bring the knees closer toward the chest during the mountain climber."

            if left_knee_status == "KNEE DOWN" and right_knee_status == "KNEE DOWN":
                return "The user is not bringing either knee forward — drive the knees toward the chest."

        elif exercise == "Plank":
            form_status = metrics.get("form_status", "")
            
            if form_status == "HIPS TOO LOW":
                return "The user's hips are dropping too low during the plank — keep the body in a straight line."

            if form_status == "HIPS TOO HIGH":
                return "The user's hips are too high during the plank — lower them to maintain a straight body line."

        return None

    def process_event(self, event, exercise, metrics):
        issue = self._find_form_issue(exercise, metrics)

        now = time.time()

        is_major_issue = event in ["workout_started", "set_completed", "workout_completed"]

        if not is_major_issue:
            if not issue:
                return None
            
            if now - self.last_spoken_at < 5:
                return None
            
        text = self.llm.give_feedback(event, issue)
        voice = self.tts.speak(text)

        self.last_spoken_at = now

        return voice, text
    



def autoplay_audio(audio_bytes):
    if not audio_bytes:
        return
    
    st.markdown("<style>[data-testid='stAudio'] {display: none;}</style>", unsafe_allow_html=True)
    
    st.audio(audio_bytes, format="audio/mp3", autoplay=True)