from services.config.workout_config import PROMPT


class LLMCoach:
    def __init__(self, openai_client):
        self.client = openai_client
        self.history = []
        self.system_prompt = PROMPT

    def give_feedback(self, event, issue):
        prompt = f"Event: {event}"

        if issue:
            prompt += f" Form Issue: {issue}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history[-10:],
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model="gpt-5.5",
            messages=messages
        )

        text = response.choices[0].message.content.strip()
        self.history.append({"role": "assistant", "content": text})

        return text
    