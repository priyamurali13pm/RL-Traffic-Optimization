from openai import OpenAI
import os
print("FILE STARTED")

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
     HF_TOKEN = "dummy"
    #raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def run():
    success = False
    rewards = []
    steps = 0

    try:
        print(f"[START] task=traffic env=custom model={MODEL_NAME}")

        # 👉 IMPORT ENV HERE
        from openenv import Env

        env = Env()

        # 👉 RESET CALLED HERE (IMPORTANT)
        state = env.reset()

        steps = 1
        action = 1

        result = env.step(action)

        reward = result["reward"]
        done = result["terminated"]

        rewards.append(reward)

        print(
            f"[STEP] step={steps} action=lane_{action} "
            f"reward={reward:.2f} done={str(done).lower()} error=null"
        )

        success = True

    except Exception as e:
        success = False

    finally:
        rewards_str = ",".join(str(r) for r in rewards) if rewards else "0.0"
        print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}")

if __name__ == "__main__":
    run()        