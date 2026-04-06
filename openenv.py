class Env:
    def __init__(self):
        self.state = [0, 0, 0, 0]
        self.step_count = 0
        self.max_steps = 50

    def reset(self):
        self.state = [0, 0, 0, 0]
        self.step_count = 0

        return {
            "observation": self.state,
            "reward": 0.0,
            "terminated": False,
            "truncated": False,
            "info": {}
        }

    def step(self, action):
        self.step_count += 1

        # simple transition
        self.state = [min(x + 1, 10) for x in self.state]

        done = self.step_count >= self.max_steps

        return {
            "observation": self.state,
            "reward": 1.0,
            "terminated": done,
            "truncated": False,
            "info": {}
        }