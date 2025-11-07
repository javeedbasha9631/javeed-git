"""
chatbot.py

Provides a lightweight EmpathyChatbot class. It will try to use Hugging Face Transformers (DialoGPT)
when available and fall back to a rule-based empathetic responder otherwise.
"""
from typing import Optional
import random

try:
    from transformers import pipeline
except Exception:
    pipeline = None


class EmpathyChatbot:
    def __init__(self):
        self.generator = None
        if pipeline is not None:
            try:
                # Try a small conversational model (DialoGPT-small). This may download weights the first time.
                self.generator = pipeline('text-generation', model='microsoft/DialoGPT-small')
            except Exception:
                self.generator = None

        # Simple template replies
        self.templates = [
            "I understand how you feel. Want to talk about it?",
            "That must be tough — take a deep breath, you’re doing great.",
            "I'm here for you. Would you like to tell me more?",
            "It sounds like that was hard. It's okay to feel this way.",
            "You're not alone in this. I'm listening."
        ]

    def respond(self, user_text: str) -> str:
        """Return an empathetic response to the user's text.

        If a generator is available, use it to produce a reply. Otherwise pick a template and adapt it.
        """
        if not user_text:
            return "Hi — I'm EmpathAI. How are you feeling today?"

        # Keyword heuristics for empathetic prompts
        lower = user_text.lower()
        if any(k in lower for k in ["sad", "depressed", "unhappy", "cry"]):
            return "I'm sorry that you're feeling sad. Do you want to share what's making you feel this way?"
        if any(k in lower for k in ["anxious", "anxiety", "worried", "scared"]):
            return "That sounds stressful. Try taking a slow breath with me. Would you like some grounding tips?"
        if any(k in lower for k in ["happy", "great", "good", "awesome"]):
            return "That's wonderful to hear — tell me more about what's going well!"

        # Use generator when available for more personalized output
        if self.generator is not None:
            try:
                out = self.generator(user_text, max_length=60, num_return_sequences=1)
                if out and isinstance(out, list):
                    text = out[0].get('generated_text', '').strip()
                    # Post-process: keep short, appending an empathetic line if needed
                    if len(text) > 0:
                        return text
            except Exception:
                pass

        # Fallback: friendly templated response
        return random.choice(self.templates)


if __name__ == "__main__":
    bot = EmpathyChatbot()
    print(bot.respond("I'm feeling very anxious about a presentation"))
