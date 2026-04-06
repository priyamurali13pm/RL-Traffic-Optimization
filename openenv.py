class Env:
    def __init__(self):
        self.state = [0, 0, 0, 0]
        self.steps = 0

    def reset(self):
        self.state = [0, 0, 0, 0]
        self.steps = 0

        return {
            "observation": self.state,
            "info": {}
        }

    def step(self, action):
        self.steps += 1

        self.state = [1, 2, 3, 4]

        return {
            "observation": self.state,
            "reward": 1.0,
            "terminated": self.steps >= 50,
            "truncated": False,
            "info": {}
        }