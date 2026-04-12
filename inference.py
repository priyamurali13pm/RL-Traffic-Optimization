import urllib.request
import urllib.request
import urllib.parse
import random
import json
import os
import re

BASE_URL = "https://priyamurali13pm-rl-traffic-optimization.hf.space"

def post_request(url, params=None):
    if params:
        query = urllib.parse.urlencode(params)
        url = f"{url}?{query}"

    req = urllib.request.Request(url, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())

    except urllib.error.HTTPError as e:
        print("[SERVER ERROR BODY]", e.read().decode(), flush=True)
        raise e

def get_action(state):
    try:
        from openai import OpenAI

        client = OpenAI(
            base_url=os.environ.get("API_BASE_URL"),
            api_key=os.environ.get("API_KEY")
        )

        prompt = f"""
        Traffic in lanes: {state}
        Which lane (0-3 should get green signal?
        Return only a number.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        output = response.choices[0].message.content
        return int(re.findall(r'\d+', output)[0])

    except Exception:
        # fallback (VERY IMPORTANT)
        return int(state.index(max(state)))    
def run():
    print("[START] task=traffic", flush=True)

    try:
        data = post_request(f"{BASE_URL}/reset")
        state = data.get("observation", [0, 0, 0, 0])

        total_reward = 0
        epsilon = 0.15  # 🔥 define here

        for step in range(5):

            # 🔥 REPLACE ONLY THIS PART
            if random.random() < epsilon:
                action = random.randint(0, len(state) - 1)
            else:
                action = get_action(state)
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