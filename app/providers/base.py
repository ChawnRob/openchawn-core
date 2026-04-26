class BaseProvider:
    def is_available(self):
        return False

    def generate(self, prompt, user_id="", system_prompt=""):
        return ""
