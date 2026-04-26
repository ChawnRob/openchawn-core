def learn_from_exchange(question, answer, provider="", tier=""):
    if len(answer) < 30:
        return None
    if "[ERREUR]" in answer:
        return None

    class Memory:
        def __init__(self):
            self.type = "fact"
            self.importance_score = 0.70
            self.source = f"auto_learn:{provider}"

    return Memory()
