import os
import json
from openai import OpenAI

# 1. Grab your token (Using the local file auto-injection method)
try:
    with open('/tmp/jwt', 'r') as f:
        CDP_TOKEN = json.load(f)['access_token']
except Exception:
    CDP_TOKEN = os.environ.get("CDP_TOKEN", "your_fallback_token")

# 2. Configure the client
client = OpenAI(
    base_url="https://gab.serving-apps.ml-64288d82-5dd.go01-dem.ylcu-atmi.cloudera.site/v1",
    api_key=CDP_TOKEN
)

print("📡 Initiating streaming response from Cloudera AI Application...\n")

# 3. Request the stream
response = client.chat.completions.create(
    model="llama-3.2",
    messages=[
        {"role": "system", "content": "You are a witty, helpful assistant."},
        {"role": "user", "content": "Write a short poem about running LLMs on CPUs."}
    ],
    temperature=0.7,
    stream=True  # 👈 Activates streaming
)

# 4. Print chunks in real-time as they land
for chunk in response:
    # Safely extract the token fragment
    token = chunk.choices[0].delta.content
    if token:
        print(token, end="", flush=True)

print("\n\n✅ Stream complete.")