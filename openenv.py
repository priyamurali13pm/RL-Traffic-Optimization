class Env:
    def __init__(self):
        self.state = [0, 0, 0, 0]

    def reset(self):
        return {
            "observation": self.state,
            "info": {}
        }

    def step(self, action):
        return {
            "observation": [1, 2, 3, 4],
            "reward": 1.0,
            "terminated": False,
            "truncated": False,
            "info": {}
        }