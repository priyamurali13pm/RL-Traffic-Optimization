class Env:
    def reset(self):
        return {
            "observation": [0, 0, 0, 0],
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