class TrafficEnv:
    def __init__(self):
        self.state = [0, 0, 0, 0]
        self.step_count = 0
        self.max_steps = 50

    def reset(self):
        self.state = [0, 0, 0, 0]
        self.step_count = 0
        return {
            "observation": self.state,
            "info": {}
        }

    def step(self, action):
        self.step_count += 1

        # dummy transition
        self.state = [1, 2, 3, 4]

        return {
            "observation": self.state,
            "reward": 1.0,
            "terminated": self.step_count >= self.max_steps,
            "truncated": False,
            "info": {}
        }