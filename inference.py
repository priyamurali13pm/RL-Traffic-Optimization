import urllib.request
import json

BASE_URL = "https://priyamurali13pm-rl-traffic-optimization.hf.space"

def post_request(url, params=None):
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query}"

    req = urllib.request.Request(url, method="POST")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def run():
    print("[START] task=traffic", flush=True)

    try:
        data = post_request(f"{BASE_URL}/reset")
        state = data.get("observation", [0, 0, 0, 0])

        total_reward = 0

        for step in range(5):
            # simple local logic
            action = state.index(max(state))

            data = post_request(f"{BASE_URL}/step", {"action": action})

            state = data.get("observation", [0, 0, 0, 0])
            reward = data.get("reward", 0)
            done = data.get("done", False)

            total_reward += reward

            print(f"[STEP] step={step+1} action={action} reward={reward}", flush=True)

            if done:
                break

        print(f"[END] total_reward={total_reward}", flush=True)

    except Exception as e:
        print("[ERROR]", str(e), flush=True)


if __name__ == "__main__":
    run()