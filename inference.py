import urllib.request
import json
import os
import re
from openai import OpenAI

# 🔥 STRICT LLM SETUP (NO .get, NO fallback)
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

BASE_URL = "https://priyamurali13pm-rl-traffic-optimization.hf.space"

# API call helper
def post_request(url):
    req = urllib.request.Request(url, method="POST")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

# LLM decision (MANDATORY)
def get_action(state):
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

    output = response.choices[0].message.content
    action = int(re.findall(r'\d+', output)[0])

    return action

def run():
    print("[START] task=traffic", flush=True)

    try:
        # RESET
        data = post_request(f"{BASE_URL}/reset")
        state = data["observation"]

        total_reward = 0
        steps = 5

        for step in range(1, steps + 1):
            action = get_action(state)

            data = post_request(f"{BASE_URL}/step?action={action}")

            reward = data.get("reward", 0)
            state = data.get("observation", state)

            total_reward += reward

            print(f"[STEP] step={step} reward={reward}", flush=True)

        # score normalization
        score = max(0, min(1, (total_reward + 100) / 100))

        print(f"[END] task=traffic score={score} steps={steps}", flush=True)

    except Exception as e:
        print(f"[END] task=traffic score=0 steps=0", flush=True)


if __name__ == "__main__":
    run()