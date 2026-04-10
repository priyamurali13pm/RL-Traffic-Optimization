import urllib.request
import json

BASE_URL = "https://priyamurali13pm-rl-traffic-optimization.hf.space"

def post_request(url):
    req = urllib.request.Request(url, method="POST")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def run():
    success = False
    rewards = []
    steps = 0

    try:
        print("[START] task=traffic env=api")

        # RESET
        data = post_request(f"{BASE_URL}/reset")
        state = data["observation"]

        total_steps = 5

        for step in range(1, total_steps + 1):
            action = state.index(max(state))

            data = post_request(f"{BASE_URL}/step?action={action}")
            print("DEBUG STEP RESPONSE:", data)

            reward = data.get("reward", 0)
            done = data.get("done", False)
            state = data.get("observation", state)

            rewards.append(reward)
            steps = step

            print(
                f"[STEP] step={step} action=lane_{action} "
                f"reward={reward:.2f} done={str(done).lower()} error=null"
            )

            if done:
                break

        success = True

    except Exception as e:
        print(f"[ERROR] {e}")
        success = False

    finally:
        rewards_str = ",".join(str(r) for r in rewards) if rewards else "0.0"
        print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}")


if __name__ == "__main__":
    run()