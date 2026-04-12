import urllib.request
import urllib.parse
import json
import random

BASE_URL = "https://priyamurali13pm-rl-traffic-optimization.hf.space"

def post_request(url, params=None):
    if params:
        query = urllib.parse.urlencode(params)
        url = f"{url}?{query}"

    req = urllib.request.Request(url, method="POST")

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def run():
    print("[START] task=traffic env=api model=local", flush=True)

    total_reward = 0
    rewards_list = []
    success = False

    try:
        data = post_request(f"{BASE_URL}/reset")
        state = data.get("observation", [0, 0, 0, 0])

        epsilon = 0.15

        for step in range(1, 6):

            # epsilon-greedy
            if random.random() < epsilon:
                action = random.randint(0, len(state) - 1)
            else:
                action = int(state.index(max(state)))

            data = post_request(f"{BASE_URL}/step", {"action": action})

            state = data.get("observation", [0, 0, 0, 0])
            reward = float(data.get("reward", 0))
            done = data.get("done", False)

            total_reward += reward
            rewards_list.append(f"{reward:.2f}")

            print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null", flush=True)

            if done:
                success = True
                break

        print(f"[END] success={str(success).lower()} steps={len(rewards_list)} rewards={','.join(rewards_list)}", flush=True)

    except Exception as e:
        print(f"[END] success=false steps=0 rewards= error={str(e)}", flush=True)


if __name__ == "__main__":
    run()