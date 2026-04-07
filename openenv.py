class Env:
    def __init__(self):
        self.task = None

    def reset(self):
        self.task = "Control traffic signal efficiently"
        return {
            "observation": self.task
        }

    def step(self, action):
        # Accept ANY action (important)
        try:
            action_str = str(action)
        except:
            action_str = ""

        reward = 1.0  # always positive

        return {
            "observation": self.task,
            "reward": float(reward),
            "terminated": True,
            "info": {}
        }