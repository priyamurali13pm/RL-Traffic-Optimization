import urllib.request   
import json
import os
from openai import OpenAI

# LLM setup
base_url = os.environ.get("API_BASE_URL")
api_key = os.environ.get("API_KEY")

if base_url and api_key:
    client = OpenAI(base_url=base_url, api_key=api_key)
else:
    client = None 

BASE_URL = "https://priyamurali13pm-rl-traffic-optimization.hf.space"

# API call helper
def post_request(url):
    req = urllib.request.Request(url, method="POST")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

# LLM decision
def get_action(state):
    if client is None:
        return state.index(max(state))  # fallback

    prompt = f"""
    You are a traffic controller.
    Traffic in lanes: {state}
    Which lane (0-3) should get green signal?
    Return only a number (0, 1, 2, or 3).
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return int(response.choices[0].message.content.strip())

def run():
    success = False
    rewards = []
    steps = 0

    try:
        print("[START] task=traffic env=api")

        # RESET
        data = post_request(f"{BASE_URL}/reset")
        state = data["observation"]
        print("RESET RESPONSE:", data)

        total_steps = 5

        for step in range(1, total_steps + 1):
            action = get_action(state)  

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